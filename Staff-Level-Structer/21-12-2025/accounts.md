### 👤 ACCOUNTS DOMAIN — BUYERS · SELLERS · AUTH · TRUST

This domain answers one question only:
“Who are you, and how much should the system trust you?”

Money, orders, coupons, shipping — all depend on this.

🧠 MENTAL MODEL (VERY IMPORTANT)

Think psychologically (since you want to master psychology 🧠):

Human Mind	System
Identity	Account
Memory	Credentials
Intent	Roles
Reputation	Trust Score
History	Audit Trail
Trauma / Abuse	Fraud Flags

👉 You never mix identity with behavior.
A user can change behavior — identity must remain stable.

### core/
└── domains/
    └── accounts/
        ├── domain/
        │   ├── aggregates/
        │   │   ├── account_aggregate.py          # ROOT OF TRUTH
        │   │   └── trust_profile_aggregate.py
        │   │
        │   ├── entities/
        │   │   ├── account.py
        │   │   ├── buyer_profile.py
        │   │   ├── seller_profile.py
        │   │   ├── credential.py
        │   │   ├── role.py
        │   │   ├── device.py
        │   │   ├── session.py
        │   │   ├── verification.py
        │   │   └── trust_signal.py
        │   │
        │   ├── value_objects/
        │   │   ├── account_id.py
        │   │   ├── email.py
        │   │   ├── phone.py
        │   │   ├── password_hash.py
        │   │   ├── role_type.py
        │   │   ├── account_status.py
        │   │   ├── trust_score.py
        │   │   ├── kyc_level.py
        │   │   └── risk_level.py
        │   │
        │   ├── domain_events/
        │   │   ├── account_created.py
        │   │   ├── account_verified.py
        │   │   ├── role_assigned.py
        │   │   ├── login_success.py
        │   │   ├── login_failed.py
        │   │   ├── account_locked.py
        │   │   ├── trust_score_updated.py
        │   │   ├── seller_upgraded.py
        │   │   └── account_suspended.py
        │   │
        │   ├── domain_services/
        │   │   ├── authentication_service.py
        │   │   ├── authorization_service.py
        │   │   ├── trust_evaluation_service.py
        │   │   ├── kyc_service.py
        │   │   └── session_management_service.py
        │   │
        │   ├── policies/
        │   │   ├── password_policy.py
        │   │   ├── account_lock_policy.py
        │   │   ├── role_escalation_policy.py
        │   │   ├── seller_onboarding_policy.py
        │   │   └── trust_decay_policy.py
        │   │
        │   └── exceptions/
        │       ├── authentication_failed.py
        │       ├── account_locked.py
        │       ├── insufficient_trust.py
        │       └── role_violation.py
        │
        ├── application/
        │   ├── use_cases/
        │   │   ├── register_account/
        │   │   ├── login/
        │   │   ├── logout/
        │   │   ├── assign_role/
        │   │   ├── verify_account/
        │   │   ├── upgrade_seller/
        │   │   ├── lock_account/
        │   │   └── evaluate_trust/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   ├── auth_command_port.py
        │   │   │   └── account_query_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── account_repository.py
        │   │       ├── session_store_port.py
        │   │       ├── notification_port.py
        │   │       ├── fraud_service_port.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── account_dto.py
        │       ├── auth_result_dto.py
        │       └── trust_profile_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── auth_views.py
        │   │   │   ├── account_views.py
        │   │   │   ├── serializers.py
        │   │   │   └── urls.py
        │   │   │
        │   │   ├── admin/
        │   │   │   └── account_admin.py
        │   │   │
        │   │   └── consumer/
        │   │       ├── order_events_handler.py
        │   │       ├── payment_events_handler.py
        │   │       └── coupon_events_handler.py
        │   │
        │   └── outbound/
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── account_model.py
        │       │   │   ├── credential_model.py
        │       │   │   ├── role_model.py
        │       │   │   ├── trust_profile_model.py
        │       │   │   ├── session_model.py
        │       │   │   └── device_model.py
        │       │   │
        │       │   ├── mappers/
        │       │   │   ├── account_mapper.py
        │       │   │   └── trust_mapper.py
        │       │   │
        │       │   └── account_repository_impl.py
        │       │
        │       ├── security/
        │       │   ├── password_hasher.py
        │       │   ├── jwt_provider.py
        │       │   └── token_blacklist.py
        │       │
        │       ├── cache/
        │       │   └── session_cache.py
        │       │
        │       └── messaging/
        │           ├── account_event_publisher.py
        │           └── account_event_consumer.py
        │
        ├── saga/
        │   └── seller_onboarding_saga.py
        │
        ├── read_model/
        │   ├── projections/
        │   │   ├── account_summary_projection.py
        │   │   ├── seller_reputation_projection.py
        │   │   └── buyer_activity_projection.py
        │   │
        │   └── rebuild/
        │       └── rebuild_account_read_model.py
        │
        ├── outbox/
        │   └── account_outbox_model.py
        │
        ├── tests/
        │   ├── domain/
        │   ├── application/
        │   ├── saga/
        │   └── adapters/
        │
        └── docs/
            ├── README.md
            ├── trust_model.md
            ├── seller_onboarding.md
            ├── auth_flows.md
            ├── threat_model.md
            └── adr.md
 
 🔐 AUTHENTICATION FLOW (ZERO TRUST)
LoginRequest
   ↓
CredentialsValidated
   ↓
DeviceRecorded
   ↓
SessionCreated
   ↓
LoginSuccess

Failure Path
LoginFailed
   ↓
RiskIncreased
   ↓
AccountLocked (policy-based)

🧬 TRUST SCORE (THIS IS GOLD)
Inputs:

Order success rate

Refund ratio

Coupon abuse

Payment failures

Device changes

IP risk

Seller disputes

Outputs:

Max order value

Coupon eligibility

Seller privileges

Payment methods

Manual review flag

Trust is dynamic — never static.

🏪 BUYER vs SELLER (STRICT SEPARATION)

One Account

Multiple Roles

Separate profiles

Shared trust score

This prevents:

Seller fraud hiding behind buyer account

Identity duplication

Cross-role abuse

📊 CORE TABLES (PRODUCTION)
account

id

email

phone

status

created_at

credential

account_id

password_hash

last_changed_at

role

account_id

role_type (BUYER, SELLER, ADMIN)

trust_profile

account_id

trust_score

risk_level

kyc_level

session

id

account_id

device_id

expires_at

🚨 NON-NEGOTIABLE INVARIANTS

Auth never trusts frontend

Trust score affects pricing & coupons

Seller onboarding is staged

Account locks propagate instantly

Sessions are revocable

Every action is auditable

🧠 WHY THIS IS STAFF-LEVEL

Identity ≠ Behavior

Trust is first-class

Event-driven security

Cross-domain influence (orders, coupons, payments)

Psychological realism (humans change, identity doesn’t)
