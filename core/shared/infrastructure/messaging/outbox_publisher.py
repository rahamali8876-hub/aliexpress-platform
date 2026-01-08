# filename : core/shared/infrastructure/messaging/outbox_publisher.py
import time
import logging
from typing import Optional
from django.db import transaction
from django.utils import timezone
import socket
from django.db.models import Min, Max
from django.db import models
from core.shared.models.outbox_event import OutboxEvent
from core.shared.infrastructure.messaging.broker.kafka_producer import get_kafka_producer
from core.shared.infrastructure.messaging.outbox.outbox_processor import OutboxProcessor

from core.shared.observability.metrics.outbox_metrics import (
    EVENTS_PROCESSED_COUNTER,
    EVENTS_FAILED_COUNTER,
)


logger = logging.getLogger(__name__)


class OutboxPublisher:
    """
    Staff-grade Outbox → Kafka orchestrator.

    Responsibilities:
    1. Poll pending Outbox events
    2. Publish them via Kafka with aggregate_id key
    3. Mark PUBLISHED only after ACK
    4. Retry failed events safely
    5. Support multiple workers
    6. Expose metrics and observability
    """

    ...

    def __init__(
        self,
        batch_size: int = 50,
        poll_interval: float = 1.0,  # seconds
        max_retries: int = 5,
        producer=None,
    ):
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self.producer = producer or get_kafka_producer()
        self.processor = OutboxProcessor(producer=self.producer)

        self.running = False

    def run_once(self):
        """
        Process a single batch of outbox events and exit.
        Useful for cron jobs, manual runs, or debugging.
        """
        logger.info("OutboxPublisher run_once started")

        try:
            self._process_batch()
        except Exception:
            logger.exception("OutboxPublisher run_once failed")

    def start(self):
        """
        Starts the publisher loop.
        Can be called from a management command or background worker.
        """
        self.running = True
        logger.info("OutboxPublisher started")

        while self.running:
            try:
                self._process_batch()
            except Exception:
                logger.exception("Unexpected error in OutboxPublisher loop")

            time.sleep(self.poll_interval)

    def stop(self):
        """Graceful shutdown"""
        self.running = False
        logger.info("OutboxPublisher stopping...")

    # def _process_batch(self):
    #     with transaction.atomic():
    #         logging.debug("Fetching pending outbox events")
    #         events = list(
    #             OutboxEvent.objects.select_for_update(skip_locked=True)
    #             .filter(status="PENDING", retry_count__lt=self.max_retries)
    #             .order_by("created_at")[: self.batch_size]
    #         )

    #     if not events:
    #         logger.debug("No pending outbox events found")
    #         return

    #     # 🔥 ONE-TIME BATCH LOG
    #     logger.info(
    #         "Outbox batch picked for publishing",
    #         extra={
    #             "batch_size": len(events),
    #             "event_ids": [str(e.id) for e in events[:5]],  # first 5 only
    #             "oldest_event_at": events[0].created_at.isoformat(),
    #             "newest_event_at": events[-1].created_at.isoformat(),
    #             "max_retry_in_batch": max(e.retry_count for e in events),
    #             "worker": socket.gethostname(),
    #         },
    #     )

    #     for event in events:
    #         self._process_event(event)

    def _process_batch(self):
        worker_id = socket.gethostname()

        with transaction.atomic():
            events = list(
                OutboxEvent.objects.select_for_update(skip_locked=True)
                .filter(
                    status=OutboxEvent.STATUS_PENDING,
                    retry_count__lt=self.max_retries,
                )
                .order_by("created_at")[: self.batch_size]
            )

            if not events:
                return

            OutboxEvent.objects.filter(id__in=[e.id for e in events]).update(
                status="PROCESSING",
                processing_owner=worker_id,
                processing_started_at=timezone.now(),
            )

        # 🚨 locks released here — SAFE
        for event in events:
            self._process_event(event, worker_id)

    # def _process_event(self, event: OutboxEvent):
    #     """
    #     Publish a single event with:
    #     - Exactly-once delivery
    #     - Aggregate-keyed Kafka partitioning
    #     - Retry handling
    #     - Metrics logging
    #     """
    #     try:
    #         # self.processor._publish_event(event)  # staff-grade atomic & ack
    #         self.processor.publish(event)

    #         # ✅ Metrics
    #         EVENTS_PROCESSED_COUNTER.inc()

    #     except Exception:
    #         # Retry counter + fail logic
    #         event.retry_count += 1
    #         if event.retry_count >= self.max_retries:
    #             event.status = "FAILED"
    #             logger.error("Outbox event moved to FAILED: %s", event.id)
    #             EVENTS_FAILED_COUNTER.inc()
    #         event.save(update_fields=["retry_count", "status"])
    #         logger.exception("Failed to publish outbox event %s", event.id)
    
    def _process_event(self, event: OutboxEvent, worker_id: str):
        try:
            self.processor.publish(event)

            updated = OutboxEvent.objects.filter(
                id=event.id,
                status="PROCESSING",
                processing_owner=worker_id,
            ).update(
                status=OutboxEvent.STATUS_PUBLISHED,
                published_at=timezone.now(),
                processing_started_at=None,
            )

            if updated != 1:
                logger.warning(
                    "Lost ownership while publishing outbox event %s", event.id
                )

            EVENTS_PROCESSED_COUNTER.inc()

        except Exception:
            OutboxEvent.objects.filter(
                id=event.id,
                status="PROCESSING",
                processing_owner=worker_id,
            ).update(
                status=OutboxEvent.STATUS_PENDING,
                retry_count=models.F("retry_count") + 1,
                processing_owner=None,
                processing_started_at=None,
            )

            EVENTS_FAILED_COUNTER.inc()
            logger.exception("Failed to publish outbox event %s", event.id)
