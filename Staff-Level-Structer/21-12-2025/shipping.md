### 🚚 SHIPPING DOMAIN — HOLY GRAIL BLUEPRINT

(Multi-carrier, SLA-driven, traceable forever)

🧠 SHIPPING MENTAL MODEL (READ THIS)

Shipping does NOT:

❌ Decide inventory

❌ Own orders

❌ Own payments

Shipping DOES:

Own delivery promises

Own carrier contracts

Own tracking truth

Own SLA compliance

Emit logistics events

Shipping is asynchronous by nature.
Never block checkout on shipping fulfillment.

### core/
└── domains/
    └── shipping/
        ├── domain/                              # PURE LOGISTICS LOGIC
        │   ├── aggregates/
        │   │   └── shipment_aggregate.py        # One shipment = one delivery promise
        │   │
        │   ├── entities/
        │   │   ├── shipment.py
        │   │   ├── shipment_item.py
        │   │   ├── tracking_event.py
        │   │   ├── carrier.py
        │   │   ├── delivery_address.py
        │   │   └── shipping_label.py
        │   │
        │   ├── value_objects/
        │   │   ├── shipment_id.py
        │   │   ├── tracking_number.py
        │   │   ├── shipment_status.py          # CREATED, PICKED, IN_TRANSIT, DELIVERED
        │   │   ├── shipping_method.py
        │   │   ├── carrier_code.py
        │   │   ├── sla_window.py
        │   │   ├── weight.py
        │   │   └── dimensions.py
        │   │
        │   ├── domain_events/                  # EVENT SOURCE OF TRUTH
        │   │   ├── shipment_created.py
        │   │   ├── shipment_assigned.py
        │   │   ├── shipment_picked_up.py
        │   │   ├── shipment_in_transit.py
        │   │   ├── shipment_delivered.py
        │   │   ├── shipment_delayed.py
        │   │   ├── shipment_lost.py
        │   │   └── shipment_returned.py
        │   │
        │   ├── domain_services/
        │   │   ├── carrier_selection_service.py
        │   │   ├── sla_evaluation_service.py
        │   │   ├── tracking_update_service.py
        │   │   └── shipping_cost_service.py
        │   │
        │   ├── policies/
        │   │   ├── sla_policy.py
        │   │   ├── carrier_fallback_policy.py
        │   │   └── reroute_policy.py
        │   │
        │   └── exceptions/
        │       ├── invalid_shipment_state.py
        │       ├── carrier_unavailable.py
        │       ├── label_generation_failed.py
        │       └── tracking_update_error.py
        │
        ├── application/                        # USE CASES
        │   ├── use_cases/
        │   │   ├── create_shipment/
        │   │   ├── assign_carrier/
        │   │   ├── generate_label/
        │   │   ├── mark_picked_up/
        │   │   ├── update_tracking/
        │   │   ├── mark_delivered/
        │   │   ├── mark_lost/
        │   │   └── initiate_return/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   ├── shipping_command_port.py
        │   │   │   └── shipping_query_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── shipment_repository.py
        │   │       ├── carrier_gateway_port.py
        │   │       ├── order_service_port.py
        │   │       ├── inventory_service_port.py
        │   │       ├── notification_service_port.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── shipment_dto.py
        │       ├── tracking_dto.py
        │       └── sla_status_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── shipping_views.py
        │   │   │   ├── shipping_serializers.py
        │   │   │   └── shipping_urls.py
        │   │   │
        │   │   ├── admin/
        │   │   │   └── shipping_admin.py
        │   │   │
        │   │   └── consumer/
        │   │       ├── order_event_handler.py
        │   │       ├── inventory_event_handler.py
        │   │       └── carrier_webhook_handler.py
        │   │
        │   └── outbound/
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── shipment_model.py
        │       │   │   ├── shipment_item_model.py
        │       │   │   ├── tracking_event_model.py
        │       │   │   └── carrier_model.py
        │       │   │
        │       │   ├── mappers/
        │       │   │   ├── shipment_mapper.py
        │       │   │   ├── tracking_mapper.py
        │       │   │   └── carrier_mapper.py
        │       │   │
        │       │   └── shipment_repository_impl.py
        │       │
        │       ├── messaging/
        │       │   ├── shipping_event_publisher.py
        │       │   └── shipping_event_consumer.py
        │       │
        │       └── carriers/                   # PLUGGABLE CARRIERS
        │           ├── fedex_adapter.py
        │           ├── dhl_adapter.py
        │           ├── ups_adapter.py
        │           └── local_courier_adapter.py
        │
        ├── saga/                               # LONG-RUNNING LOGISTICS
        │   ├── shipment_fulfillment_saga.py
        │   └── return_saga.py
        │
        ├── outbox/                             # RELIABLE DELIVERY
        │   └── shipping_outbox_model.py
        │
        ├── read_model/                         # CUSTOMER-FACING VIEWS
        │   ├── projections/
        │   │   ├── shipment_tracking_projection.py
        │   │   ├── delivery_timeline_projection.py
        │   │   └── seller_shipping_projection.py
        │   │
        │   ├── tables/
        │   │   ├── shipment_tracking_table.sql
        │   │   ├── delivery_timeline_table.sql
        │   │   └── seller_shipping_table.sql
        │   │
        │   └── rebuild/
        │       └── rebuild_shipping_read_model.py
        │
        ├── tests/
        │   ├── domain/
        │   ├── application/
        │   ├── saga/
        │   └── adapters/
        │
        └── docs/
            ├── README.md
            ├── sla_model.md
            ├── carrier_integration.md
            ├── failure_scenarios.md
            └── adr.md


🔁 SHIPPING EVENT FLOWS
📦 ORDER → DELIVERY
OrderConfirmed
   ↓
ShipmentCreated
   ↓
CarrierAssigned
   ↓
LabelGenerated
   ↓
PickedUp
   ↓
InTransit
   ↓
Delivered

⏱️ SLA BREACH FLOW
SLAExceeded
   ↓
ShipmentDelayed
   ↓
CustomerNotified
   ↓
CompensationTriggered

❌ FAILURE FLOW
CarrierLostPackage
   ↓
ShipmentLost
   ↓
OrderRefundInitiated
   ↓
InventoryAdjusted

🧬 CORE DATABASE TABLES
shipment

id

order_id

carrier_code

tracking_number

status

sla_deadline

created_at

delivered_at

tracking_event

id

shipment_id

status

location

occurred_at

carrier

id

code

name

sla_hours

active

🧠 WHY THIS IS ALIEXPRESS-GRADE

Multi-carrier abstraction

SLA tracked per shipment

Full delivery timeline

Automatic rerouting & fallback

Long-term traceability

Clean separation of concerns