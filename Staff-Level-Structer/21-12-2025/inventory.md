### 📦 INVENTORY DOMAIN — HOLY GRAIL BLUEPRINT

(Reservation-based, eventual consistency, no overselling)

🧠 INVENTORY MENTAL MODEL (IMPORTANT)

Think in three layers of truth:

1️⃣ Stock → Physical truth (what exists)
2️⃣ Reservation → Promise truth (what is temporarily held)
3️⃣ Availability → What buyers see (derived)

Inventory never trusts synchronous calls.
Everything flows via events + reservations.

### core/
└── domains/
    └── inventory/
        ├── domain/                              # PURE BUSINESS LOGIC
        │   ├── aggregates/
        │   │   └── inventory_item_aggregate.py  # SKU + Warehouse boundary
        │   │
        │   ├── entities/
        │   │   ├── inventory_item.py
        │   │   ├── stock_level.py
        │   │   ├── reservation.py
        │   │   ├── warehouse.py
        │   │   └── stock_movement.py
        │   │
        │   ├── value_objects/
        │   │   ├── sku.py
        │   │   ├── quantity.py
        │   │   ├── warehouse_id.py
        │   │   ├── reservation_id.py
        │   │   ├── inventory_status.py
        │   │   └── expiration_time.py
        │   │
        │   ├── domain_events/                   # EVENT-DRIVEN CORE
        │   │   ├── stock_added.py
        │   │   ├── stock_removed.py
        │   │   ├── stock_adjusted.py
        │   │   ├── inventory_reserved.py
        │   │   ├── inventory_released.py
        │   │   ├── inventory_committed.py
        │   │   ├── inventory_out_of_stock.py
        │   │   └── reservation_expired.py
        │   │
        │   ├── domain_services/
        │   │   ├── availability_calculation_service.py
        │   │   ├── reservation_expiry_service.py
        │   │   └── stock_validation_service.py
        │   │
        │   ├── policies/
        │   │   ├── oversell_policy.py
        │   │   ├── reservation_policy.py
        │   │   └── backorder_policy.py
        │   │
        │   └── exceptions/
        │       ├── insufficient_stock.py
        │       ├── reservation_not_found.py
        │       ├── invalid_inventory_state.py
        │       └── warehouse_closed.py
        │
        ├── application/                         # USE CASES
        │   ├── use_cases/
        │   │   ├── add_stock/
        │   │   ├── remove_stock/
        │   │   ├── adjust_stock/
        │   │   ├── reserve_inventory/
        │   │   ├── release_inventory/
        │   │   ├── commit_inventory/
        │   │   └── expire_reservations/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   ├── inventory_command_port.py
        │   │   │   └── inventory_query_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── inventory_repository.py
        │   │       ├── order_service_port.py
        │   │       ├── product_service_port.py
        │   │       ├── event_publisher_port.py
        │   │       └── clock_port.py             # TIME CONTROL (TESTABLE)
        │   │
        │   └── dto/
        │       ├── inventory_item_dto.py
        │       ├── reservation_dto.py
        │       └── availability_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── inventory_views.py
        │   │   │   ├── inventory_serializers.py
        │   │   │   └── inventory_urls.py
        │   │   │
        │   │   ├── admin/
        │   │   │   └── inventory_admin.py
        │   │   │
        │   │   └── consumer/
        │   │       ├── order_event_handler.py
        │   │       ├── payment_event_handler.py
        │   │       └── product_event_handler.py
        │   │
        │   └── outbound/
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── inventory_item_model.py
        │       │   │   ├── stock_movement_model.py
        │       │   │   ├── reservation_model.py
        │       │   │   └── warehouse_model.py
        │       │   │
        │       │   ├── mappers/
        │       │   │   ├── inventory_item_mapper.py
        │       │   │   ├── reservation_mapper.py
        │       │   │   └── warehouse_mapper.py
        │       │   │
        │       │   └── inventory_repository_impl.py
        │       │
        │       ├── messaging/
        │       │   ├── inventory_event_publisher.py
        │       │   └── inventory_event_consumer.py
        │       │
        │       └── cache/
        │           └── availability_cache_adapter.py
        │
        ├── saga/                                # CROSS-DOMAIN COORDINATION
        │   ├── inventory_reservation_saga.py
        │   └── inventory_commit_saga.py
        │
        ├── outbox/                              # DELIVERY GUARANTEE
        │   └── inventory_outbox_model.py
        │
        ├── read_model/                          # CQRS (FAST READS)
        │   ├── projections/
        │   │   ├── sku_availability_projection.py
        │   │   ├── warehouse_stock_projection.py
        │   │   └── seller_inventory_projection.py
        │   │
        │   ├── tables/
        │   │   ├── sku_availability_table.sql
        │   │   ├── warehouse_stock_table.sql
        │   │   └── seller_inventory_table.sql
        │   │
        │   └── rebuild/
        │       └── rebuild_inventory_read_model.py
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
            ├── concurrency_model.md
            └── adr.md

### 🔐 CORE INVARIANTS (NON-NEGOTIABLE)
available_quantity =
    total_stock
  - active_reservations
  - committed_quantity


Rules:

❌ Never allow negative availability

❌ Never directly reduce stock on order creation

✅ Always reserve → commit later

✅ Expire reservations automatically

🔁 EVENT FLOWS (REAL WORLD SAFE)
🛒 CHECKOUT FLOW
OrderCreated
   ↓
InventoryReserved (TTL = 15 min)
   ↓
PaymentAuthorized
   ↓
InventoryCommitted
   ↓
StockRemoved

❌ FAILURE FLOW
PaymentFailed
   ↓
InventoryReleased
   ↓
AvailabilityUpdated

⏱️ TIMEOUT FLOW
ReservationExpired
   ↓
InventoryReleased
   ↓
AvailabilityUpdated

🧬 DATABASE TABLES (STAFF-LEVEL)
inventory_item

id

sku

warehouse_id

total_stock

committed_quantity

created_at

updated_at

reservation

id

sku

warehouse_id

quantity

expires_at

order_id

status

stock_movement (AUDIT FOREVER)

id

sku

warehouse_id

quantity

movement_type (ADD / REMOVE / ADJUST)

reason

reference_id

created_at

🧠 WHY THIS SCALES TO ALIEXPRESS

No overselling under massive concurrency

Multi-warehouse aware

Saga-driven commits

Outbox guarantees

Replayable read models

Auditable for 50 years