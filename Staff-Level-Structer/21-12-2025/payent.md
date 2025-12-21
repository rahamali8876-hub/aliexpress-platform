core/
└── domains/
    └── payments/
        ├── domain/                          # PURE BUSINESS (NO GATEWAYS)
        │   ├── aggregates/
        │   │   └── payment_aggregate.py     # Transaction boundary
        │   │
        │   ├── entities/
        │   │   ├── payment.py
        │   │   ├── payment_attempt.py
        │   │   ├── refund.py
        │   │   └── payment_method_snapshot.py
        │   │
        │   ├── value_objects/
        │   │   ├── payment_id.py
        │   │   ├── payment_status.py        # INITIATED, AUTHORIZED, CAPTURED, FAILED
        │   │   ├── money.py
        │   │   ├── currency.py
        │   │   ├── gateway_reference.py
        │   │   └── idempotency_key.py
        │   │
        │   ├── domain_events/
        │   │   ├── payment_initiated.py
        │   │   ├── payment_authorized.py
        │   │   ├── payment_captured.py
        │   │   ├── payment_failed.py
        │   │   ├── refund_initiated.py
        │   │   ├── refund_completed.py
        │   │   └── refund_failed.py
        │   │
        │   ├── domain_services/
        │   │   ├── payment_validation_service.py
        │   │   ├── refund_validation_service.py
        │   │   └── payment_timeout_service.py
        │   │
        │   ├── policies/
        │   │   ├── retry_policy.py
        │   │   ├── refund_policy.py
        │   │   └── capture_policy.py
        │   │
        │   └── exceptions/
        │       ├── invalid_payment_state.py
        │       ├── duplicate_payment.py
        │       ├── refund_not_allowed.py
        │       └── gateway_timeout.py
        │
        ├── application/                     # USE CASES
        │   ├── use_cases/
        │   │   ├── initiate_payment/
        │   │   ├── authorize_payment/
        │   │   ├── capture_payment/
        │   │   ├── fail_payment/
        │   │   ├── initiate_refund/
        │   │   └── complete_refund/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   ├── payment_command_port.py
        │   │   │   └── payment_query_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── payment_repository.py
        │   │       ├── payment_gateway_port.py    # Stripe / Razorpay / PayPal
        │   │       ├── order_service_port.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── payment_dto.py
        │       └── refund_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── payment_views.py
        │   │   │   ├── payment_serializers.py
        │   │   │   └── payment_urls.py
        │   │   │
        │   │   └── consumer/
        │   │       └── order_event_handler.py
        │   │
        │   └── outbound/
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── payment_model.py
        │       │   │   ├── payment_attempt_model.py
        │       │   │   └── refund_model.py
        │       │   │
        │       │   ├── mappers/
        │       │   │   ├── payment_mapper.py
        │       │   │   └── refund_mapper.py
        │       │   │
        │       │   └── payment_repository_impl.py
        │       │
        │       ├── messaging/
        │       │   ├── payment_event_publisher.py
        │       │   └── payment_event_consumer.py
        │       │
        │       └── gateways/
        │           ├── stripe_adapter.py
        │           ├── razorpay_adapter.py
        │           └── paypal_adapter.py
        │
        ├── saga/
        │   ├── payment_authorization_saga.py
        │   └── refund_saga.py
        │
        ├── outbox/
        │   └── payment_outbox_model.py
        │
        ├── read_model/
        │   ├── projections/
        │   │   ├── payment_status_projection.py
        │   │   └── refund_projection.py
        │   │
        │   ├── tables/
        │   │   └── payment_read_table.sql
        │   │
        │   └── rebuild/
        │       └── rebuild_payment_read_model.py
        │
        ├── tests/
        │   ├── domain/
        │   ├── application/
        │   ├── adapters/
        │   └── saga/
        │
        └── docs/
            ├── README.md
            ├── invariants.md
            ├── failure_scenarios.md
            ├── pci_notes.md
            └── adr.md
