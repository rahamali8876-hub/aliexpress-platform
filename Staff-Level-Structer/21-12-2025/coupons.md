### 🎟️ COUPONS DOMAIN — HOLY GRAIL BLUEPRINT

(Pricing authority + fraud prevention)

🧠 COUPONS MENTAL MODEL (CRITICAL)

Coupons do NOT:

❌ Trust frontend totals

❌ Apply discounts blindly

❌ Modify orders directly

Coupons DO:

Validate eligibility

Calculate discounts

Lock usage atomically

Emit pricing events

Prevent abuse

Coupons never change money — they influence pricing decisions elsewhere. 

### core/
└── domains/
    └── coupons/
        ├── domain/                              # PURE PRICING RULES
        │   ├── aggregates/
        │   │   └── coupon_aggregate.py          # Coupon = rule + limits
        │   │
        │   ├── entities/
        │   │   ├── coupon.py
        │   │   ├── coupon_rule.py
        │   │   ├── coupon_usage.py
        │   │   ├── eligibility_context.py
        │   │   └── discount_application.py
        │   │
        │   ├── value_objects/
        │   │   ├── coupon_code.py
        │   │   ├── discount_type.py            # PERCENT, FIXED, SHIPPING
        │   │   ├── discount_value.py
        │   │   ├── currency.py
        │   │   ├── usage_limit.py
        │   │   ├── order_amount.py
        │   │   ├── validity_period.py
        │   │   └── fraud_score.py
        │   │
        │   ├── domain_events/
        │   │   ├── coupon_created.py
        │   │   ├── coupon_activated.py
        │   │   ├── coupon_applied.py
        │   │   ├── coupon_rejected.py
        │   │   ├── coupon_redeemed.py
        │   │   ├── coupon_released.py
        │   │   └── coupon_disabled.py
        │   │
        │   ├── domain_services/
        │   │   ├── coupon_validation_service.py
        │   │   ├── discount_calculation_service.py
        │   │   ├── eligibility_evaluation_service.py
        │   │   └── fraud_detection_service.py
        │   │
        │   ├── policies/
        │   │   ├── stacking_policy.py
        │   │   ├── per_user_limit_policy.py
        │   │   ├── minimum_order_policy.py
        │   │   ├── seller_scope_policy.py
        │   │   └── fraud_block_policy.py
        │   │
        │   └── exceptions/
        │       ├── invalid_coupon.py
        │       ├── coupon_expired.py
        │       ├── usage_limit_exceeded.py
        │       ├── not_eligible.py
        │       └── suspected_fraud.py
        │
        ├── application/                         # USE CASES
        │   ├── use_cases/
        │   │   ├── create_coupon/
        │   │   ├── activate_coupon/
        │   │   ├── validate_coupon/
        │   │   ├── apply_coupon/
        │   │   ├── redeem_coupon/
        │   │   ├── release_coupon/
        │   │   └── disable_coupon/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   ├── coupon_command_port.py
        │   │   │   └── coupon_query_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── coupon_repository.py
        │   │       ├── order_service_port.py
        │   │       ├── cart_service_port.py
        │   │       ├── account_service_port.py
        │   │       ├── fraud_service_port.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── coupon_dto.py
        │       ├── discount_result_dto.py
        │       └── eligibility_result_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── coupon_views.py
        │   │   │   ├── coupon_serializers.py
        │   │   │   └── coupon_urls.py
        │   │   │
        │   │   ├── admin/
        │   │   │   └── coupon_admin.py
        │   │   │
        │   │   └── consumer/
        │   │       ├── checkout_event_handler.py
        │   │       └── order_event_handler.py
        │   │
        │   └── outbound/
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── coupon_model.py
        │       │   │   ├── coupon_rule_model.py
        │       │   │   ├── coupon_usage_model.py
        │       │   │   └── coupon_audit_model.py
        │       │   │
        │       │   ├── mappers/
        │       │   │   ├── coupon_mapper.py
        │       │   │   ├── rule_mapper.py
        │       │   │   └── usage_mapper.py
        │       │   │
        │       │   └── coupon_repository_impl.py
        │       │
        │       ├── messaging/
        │       │   ├── coupon_event_publisher.py
        │       │   └── coupon_event_consumer.py
        │       │
        │       └── cache/
        │           └── coupon_validation_cache.py
        │
        ├── saga/                               # CHECKOUT COORDINATION
        │   └── coupon_application_saga.py
        │
        ├── outbox/                             # EVENT GUARANTEE
        │   └── coupon_outbox_model.py
        │
        ├── read_model/                         # FAST VALIDATION
        │   ├── projections/
        │   │   ├── active_coupon_projection.py
        │   │   ├── user_coupon_usage_projection.py
        │   │   └── seller_coupon_projection.py
        │   │
        │   ├── tables/
        │   │   ├── active_coupon_table.sql
        │   │   ├── user_coupon_usage_table.sql
        │   │   └── seller_coupon_table.sql
        │   │
        │   └── rebuild/
        │       └── rebuild_coupon_read_model.py
        │
        ├── tests/
        │   ├── domain/
        │   ├── application/
        │   ├── saga/
        │   └── adapters/
        │
        └── docs/
            ├── README.md
            ├── discount_rules.md
            ├── fraud_patterns.md
            ├── failure_scenarios.md
            └── adr.md
 
 🔁 COUPON EVENT FLOWS
🛒 CHECKOUT APPLY FLOW
CheckoutStarted
   ↓
CouponValidated
   ↓
CouponApplied (LOCKED)
   ↓
OrderCreated
   ↓
CouponRedeemed

❌ FAILURE / ROLLBACK FLOW
CheckoutFailed
   ↓
CouponReleased
   ↓
UsageCountRestored

🚨 FRAUD FLOW
SuspiciousUsageDetected
   ↓
CouponRejected
   ↓
CouponDisabled (optional)
   ↓
SecurityAlertRaised

🔐 CORE INVARIANTS (NON-NEGOTIABLE)

One coupon usage = atomic lock

Coupons expire by time and by count

Discount never exceeds order total

Coupon stacking explicitly controlled

Coupon is released if checkout fails

Every usage is audited forever

🧬 DATABASE TABLES (STAFF LEVEL)
coupon

id

code

discount_type

discount_value

valid_from

valid_until

max_total_uses

max_uses_per_user

active

coupon_usage

id

coupon_id

user_id

order_id

status (LOCKED / REDEEMED / RELEASED)

used_at

coupon_audit

id

coupon_id

action

reason

actor

created_at

🧠 WHY THIS IS PRODUCTION-GRADE

Abuse-resistant by design

Checkout-safe locking

Rule-based extensibility

Full forensic audit trail

Scales to flash sales

Zero money leakage