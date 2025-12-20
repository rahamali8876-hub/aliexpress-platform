
### aliexpress-api/ Project Structure
├── docker/
│   ├── django/
│   │   ├── Dockerfile
│   │   └── entrypoint.sh
│   ├── kafka/
│   │   └── Dockerfile
│   └── postgres/
│       └── Dockerfile
│
├── docker-compose.yml
├── docker-compose.override.yml
├── .env
├── .env.example
│
├── manage.py
├── requirements.txt
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── core/
│   ├── __init__.py
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   └── domain_exceptions.py
│   │   ├── messaging/
│   │   │   ├── __init__.py
│   │   │   ├── kafka_producer.py
│   │   │   ├── kafka_consumer.py
│   │   │   └── event_router.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── time.py
│   │
│   ├── domains/
│   │   ├── orders/
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── order_model.py
│   │   │   │   └── order_item_model.py
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   └── order_service.py
│   │   │   │
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── views.py
│   │   │   │   └── urls.py
│   │   │   │
│   │   │   ├── outbox/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── outbox_model.py
│   │   │   │   └── outbox_repository.py
│   │   │   │
│   │   │   ├── saga/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── checkout/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── checkout_saga.py
│   │   │   │   │   ├── checkout_state.py
│   │   │   │   │   ├── checkout_repository.py
│   │   │   │   │   └── checkout_events.py
│   │   │   │   │
│   │   │   │   └── handlers/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── inventory_reserved_handler.py
│   │   │   │       ├── inventory_failed_handler.py
│   │   │   │       ├── payment_authorized_handler.py
│   │   │   │       ├── payment_failed_handler.py
│   │   │   │       └── shipment_created_handler.py
│   │   │   │
│   │   │   └── events/
│   │   │       ├── __init__.py
│   │   │       └── order_events.py
│   │   │
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── stock_model.py
│   │   │   ├── services/
│   │   │   │   └── inventory_service.py
│   │   │   ├── consumers/
│   │   │   │   └── inventory_event_consumer.py
│   │   │   └── events/
│   │   │       └── inventory_events.py
│   │   │
│   │   ├── payments/
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   └── payment_model.py
│   │   │   ├── services/
│   │   │   │   └── payment_service.py
│   │   │   ├── consumers/
│   │   │   │   └── payment_event_consumer.py
│   │   │   └── events/
│   │   │       └── payment_events.py
│   │   │
│   │   └── shipping/
│   │       ├── __init__.py
│   │       ├── models/
│   │       │   └── shipment_model.py
│   │       ├── services/
│   │       │   └── shipping_service.py
│   │       ├── consumers/
│   │       │   └── shipping_event_consumer.py
│   │       └── events/
│   │           └── shipping_events.py
│   │
│   └── governance/
│       ├── architecture/
│       │   ├── adr_0001_domain_split.md
│       │   └── adr_0002_event_choreography.md
│       └── reviews/
│           └── review_checklist.md
│
├── scripts/
│   ├── kafka_create_topics.sh
│   └── run_consumers.py
│
├── tests/
│   ├── orders/
│   ├── inventory/
│   ├── payments/
│   └── shipping/
│
└── README.md




### core/domains/orders/
├── apps.py                     ✅ REQUIRED
├── models/                     ✅ REQUIRED
├── migrations/                 ✅ REQUIRED
│
├── adapters/
│   └── inbound/
│       └── admin/
│           ├── order_admin.py  ✅ OPTIONAL (when needed)
│           └── refund_admin.py

# core/domains/orders/apps.py
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    name = "core.domains.orders"
    label = "orders"

    def ready(self):
        from .adapters.inbound.admin import order_admin  # noqa
