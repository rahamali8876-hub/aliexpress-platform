### 🔔 NOTIFICATIONS DOMAIN

(Email · SMS · Push · In-App · WhatsApp)

Notifications answer one question only:
“Who needs to know what, when, and through which channel?”

🧠 MENTAL MODEL (PSYCHOLOGY-ALIGNED 🧠)

Human analogy (important for you):

Human Nervous System	Platform
Sensory input	Domain events
Brain filtering	Notification rules
Attention	Priority & urgency
Habituation	Rate limiting
Trauma	Spam / overload
Memory	Delivery history

👉 Bad notifications train users to ignore you.
👉 Good notifications shape behavior.

🎯 CORE PRINCIPLES (NON-NEGOTIABLE)

Event-driven only (never controller-driven)

Idempotent delivery

User-preference aware

Channel fallback supported

Fully auditable

Rate-limited per user + per event

### core/
└── domains/
    └── notifications/
        ├── domain/
        │   ├── aggregates/
        │   │   └── notification_policy_aggregate.py
        │   │
        │   ├── entities/
        │   │   ├── notification.py
        │   │   ├── notification_template.py
        │   │   ├── delivery_attempt.py
        │   │   ├── user_preference.py
        │   │   └── channel.py
        │   │
        │   ├── value_objects/
        │   │   ├── notification_id.py
        │   │   ├── channel_type.py          # EMAIL, SMS, PUSH, IN_APP
        │   │   ├── priority.py              # LOW, NORMAL, HIGH, CRITICAL
        │   │   ├── locale.py
        │   │   ├── template_key.py
        │   │   ├── delivery_status.py
        │   │   ├── retry_policy.py
        │   │   └── quiet_hours.py
        │   │
        │   ├── domain_events/
        │   │   ├── notification_created.py
        │   │   ├── notification_sent.py
        │   │   ├── notification_failed.py
        │   │   ├── notification_delayed.py
        │   │   └── notification_suppressed.py
        │   │
        │   ├── domain_services/
        │   │   ├── notification_decision_service.py
        │   │   ├── channel_selection_service.py
        │   │   ├── rate_limit_service.py
        │   │   └── template_render_service.py
        │   │
        │   ├── policies/
        │   │   ├── quiet_hours_policy.py
        │   │   ├── priority_override_policy.py
        │   │   ├── fallback_channel_policy.py
        │   │   └── suppression_policy.py
        │   │
        │   └── exceptions/
        │       ├── notification_suppressed.py
        │       ├── rate_limit_exceeded.py
        │       └── invalid_template.py
        │
        ├── application/
        │   ├── use_cases/
        │   │   ├── create_notification/
        │   │   ├── send_notification/
        │   │   ├── retry_delivery/
        │   │   └── update_preferences/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   └── notification_command_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── email_gateway_port.py
        │   │       ├── sms_gateway_port.py
        │   │       ├── push_gateway_port.py
        │   │       ├── preference_repository.py
        │   │       ├── delivery_repository.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── notification_request_dto.py
        │       └── delivery_result_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── consumer/
        │   │   │   ├── order_events_handler.py
        │   │   │   ├── payment_events_handler.py
        │   │   │   ├── shipping_events_handler.py
        │   │   │   └── account_events_handler.py
        │   │   │
        │   │   └── rest/
        │   │       ├── preference_views.py
        │   │       └── preference_serializers.py
        │   │
        │   └── outbound/
        │       ├── gateways/
        │       │   ├── email/
        │       │   │   ├── ses_gateway.py
        │       │   │   └── sendgrid_gateway.py
        │       │   │
        │       │   ├── sms/
        │       │   │   ├── twilio_gateway.py
        │       │   │   └── msg91_gateway.py
        │       │   │
        │       │   └── push/
        │       │       ├── fcm_gateway.py
        │       │       └── apns_gateway.py
        │       │
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── notification_model.py
        │       │   │   ├── template_model.py
        │       │   │   ├── delivery_attempt_model.py
        │       │   │   └── preference_model.py
        │       │   │
        │       │   └── notification_repository_impl.py
        │       │
        │       └── scheduler/
        │           └── delayed_delivery_scheduler.py
        │
        ├── saga/
        │   └── notification_delivery_saga.py
        │
        ├── outbox/
        │   └── notification_outbox_model.py
        │
        ├── read_model/
        │   ├── projections/
        │   │   ├── user_notification_stats.py
        │   │   └── delivery_health_projection.py
        │   │
        │   └── rebuild/
        │       └── rebuild_notification_read_model.py
        │
        ├── tests/
        │   ├── domain/
        │   ├── application/
        │   ├── saga/
        │   └── adapters/
        │
        └── docs/
            ├── README.md
            ├── notification_matrix.md
            ├── rate_limiting.md
            ├── templates.md
            ├── failure_modes.md
            └── adr.md


📊 NOTIFICATION MATRIX (REAL-WORLD)
Event	Priority	Channels
Order Placed	NORMAL	Email + Push
Payment Failed	HIGH	Push + Email
OTP	CRITICAL	SMS
Shipping Update	LOW	Push
Refund Issued	NORMAL	Email
Seller Violation	CRITICAL	Email + Admin Alert
🔐 USER PREFERENCES (POWERFUL)

Users can:

Disable marketing notifications

Set quiet hours

Choose channels

Select language

Mute event types

System can override only if:

Legal

Security

Financial risk

🧬 DATABASE TABLES
notification

id

account_id

template_key

priority

payload

created_at

delivery_attempt

notification_id

channel

status

error

attempted_at

user_preference

account_id

channel

enabled

quiet_hours

🚨 FAILURE MODES (PLANNED)

Gateway down → fallback channel

Rate limit hit → delay

Invalid template → suppress

User blocked → audit only

🧠 WHY THIS IS STAFF-LEVEL

No controller-level coupling

Event-driven orchestration

Psychological realism

Cost-aware (SMS ≠ Email)

Fully observable & debuggable
