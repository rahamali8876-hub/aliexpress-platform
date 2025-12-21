### ⭐ REVIEWS & RATINGS DOMAIN — HOLY GRAIL

Every piece of feedback is both data and trust currency.
This system shapes marketplace behavior, so it must be robust and auditable.

🧠 MENTAL MODEL (PSYCHOLOGY-ALIGNED)
Human Mind	Reviews System
Social proof	Rating aggregation
Bias	Weighted reviews
Reputation	Seller & product score
Attention	Featured reviews
Fraud detection	Review moderation
Learning	Verified buyer signals
🎯 CORE PRINCIPLES

Event-driven only (Reviews are reactions to Orders / Products / Deliveries)

Fraud detection (bots, fake accounts, incentivized reviews)

Weighted & normalized ratings

Verified buyer priority

Read-model heavy for aggregation

Fully auditable and reversible
 
### core/
└── domains/
    └── reviews/
        ├── domain/
        │   ├── aggregates/
        │   │   └── review_aggregate.py          # transactional boundary per product
        │   │
        │   ├── entities/
        │   │   ├── review.py
        │   │   ├── rating.py
        │   │   ├── reviewer_profile.py
        │   │   ├── moderation_action.py
        │   │   └── product_snapshot.py
        │   │
        │   ├── value_objects/
        │   │   ├── review_id.py
        │   │   ├── rating_value.py
        │   │   ├── verified_buyer_flag.py
        │   │   ├── moderation_status.py
        │   │   ├── timestamp.py
        │   │   └── fraud_score.py
        │   │
        │   ├── domain_events/
        │   │   ├── review_created.py
        │   │   ├── review_updated.py
        │   │   ├── review_deleted.py
        │   │   ├── rating_changed.py
        │   │   └── review_flagged.py
        │   │
        │   ├── domain_services/
        │   │   ├── rating_aggregation_service.py
        │   │   ├── review_validation_service.py
        │   │   ├── fraud_detection_service.py
        │   │   └── reviewer_reputation_service.py
        │   │
        │   ├── policies/
        │   │   ├── verified_buyer_policy.py
        │   │   ├── min_content_policy.py
        │   │   ├── rating_weight_policy.py
        │   │   └── moderation_policy.py
        │   │
        │   └── exceptions/
        │       ├── invalid_review.py
        │       ├── rating_out_of_bounds.py
        │       ├── fraud_detected.py
        │       └── moderation_error.py
        │
        ├── application/
        │   ├── use_cases/
        │   │   ├── submit_review/
        │   │   ├── update_review/
        │   │   ├── delete_review/
        │   │   ├── calculate_product_rating/
        │   │   ├── moderate_review/
        │   │   └── rebuild_ratings_aggregation/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   └── review_command_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── review_repository_port.py
        │   │       ├── fraud_service_port.py
        │   │       ├── notification_service_port.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── review_request_dto.py
        │       ├── review_result_dto.py
        │       └── rating_aggregation_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── review_views.py
        │   │   │   ├── review_serializers.py
        │   │   │   └── review_urls.py
        │   │   │
        │   │   └── consumer/
        │   │       ├── order_events_handler.py
        │   │       └── shipping_events_handler.py
        │   │
        │   └── outbound/
        │       ├── persistence/
        │       │   ├── models/
        │       │   │   ├── review_model.py
        │       │   │   ├── rating_model.py
        │       │   │   ├── moderation_model.py
        │       │   │   └── reviewer_profile_model.py
        │       │   │
        │       │   ├── mappers/
        │       │   │   ├── review_mapper.py
        │       │   │   └── rating_mapper.py
        │       │   │
        │       │   └── review_repository_impl.py
        │       │
        │       ├── messaging/
        │       │   ├── review_event_publisher.py
        │       │   └── review_event_consumer.py
        │       │
        │       └── cache/
        │           └── review_cache_adapter.py
        │
        ├── read_model/
        │   ├── projections/
        │   │   ├── product_rating_projection.py
        │   │   ├── top_reviews_projection.py
        │   │   └── reviewer_stats_projection.py
        │   │
        │   ├── tables/
        │   │   ├── product_rating_table.sql
        │   │   ├── top_reviews_table.sql
        │   │   └── reviewer_stats_table.sql
        │   │
        │   └── rebuild/
        │       └── rebuild_review_read_model.py
        │
        ├── saga/
        │   └── review_moderation_saga.py
        │
        ├── outbox/
        │   └── review_outbox_model.py
        │
        ├── tests/
        │   ├── domain/
        │   ├── application/
        │   ├── adapters/
        │   └── saga/
        │
        └── docs/
            ├── README.md
            ├── trust_model.md
            ├── fraud_detection.md
            ├── rating_weighting.md
            ├── moderation.md
            └── adr.md

🔁 EVENT → REVIEW FLOW
OrderCompleted
   ↓
SubmitReviewUseCase
   ↓
FraudDetectionService
   ↓
ReviewAggregate
   ↓
PersistReview
   ↓
RecalculateProductRating
   ↓
UpdateReadModel
   ↓
EventPublished

⚖️ FRAUD & MODERATION RULES

Only verified buyers can submit rating ≥ 4

Reviews with suspicious patterns → flagged

High fraud_score → hold until moderation

Automated moderation + human-in-loop

📊 RATING AGGREGATION STRATEGY

Weighted average by verified buyer / recency / product category

Separate seller rating vs product rating

Rolling average + historical snapshots for transparency

🧬 DATABASE TABLES
review

id

product_id

reviewer_id

order_id

rating

comment

created_at

updated_at

verified_buyer

fraud_score

rating_aggregation

product_id

avg_rating

total_reviews

verified_reviews

last_updated

moderation_action

review_id

action_type (suppress, approve, escalate)

moderator_id

created_at

notes

reviewer_profile

reviewer_id

total_reviews

fraud_flags

reputation_score

🚨 FAILURE MODES

Fraud → suppress silently

Rating recalculation fails → fallback to last known

Review deleted → rebuild aggregates

Moderation system down → queue for later

🧠 WHY THIS IS STAFF/PRINCIPAL LEVEL

Event-driven

Fraud & reputation aware

Weighted aggregation

Read-model heavy for scale

Fully auditable & reversible

Separation of concerns (no domain bleed)

✅ With this, your platform now has:

Products → Orders → Cart → Inventory → Checkout → Shipping → Coupons → Accounts → Notifications → Search → Reviews/Ratings