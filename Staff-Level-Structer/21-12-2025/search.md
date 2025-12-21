### 🔎 SEARCH DOMAIN — HOLY GRAIL (AliExpress-Scale)

Search never owns truth.
Search reflects truth from other domains — fast, ranked, personalized.

🧠 MENTAL MODEL (PSYCHOLOGY 🧠)
Human Mind	Search System
Memory recall	Index lookup
Attention	Ranking
Bias	Personalization
Forgetting	Index TTL
Salience	Boosting
Confusion	Poor relevance

👉 Bad search = learned helplessness
👉 Good search = dopamine loop

🎯 NON-NEGOTIABLE PRINCIPLES

Read-model only domain

Event-fed from Products, Inventory, Pricing, Shipping, Reviews

No synchronous calls from UI

Fully rebuildable from events

Ranking is a first-class citizen

Zero business logic ownership

📁 FOLDER STRUCTURE (SEARCH IS SPE

### core/
└── domains/
    └── search/
        ├── domain/
        │   ├── entities/
        │   │   ├── searchable_document.py
        │   │   ├── search_query.py
        │   │   ├── ranking_profile.py
        │   │   └── facet.py
        │   │
        │   ├── value_objects/
        │   │   ├── search_term.py
        │   │   ├── relevance_score.py
        │   │   ├── boost_factor.py
        │   │   ├── sort_order.py
        │   │   ├── filter_condition.py
        │   │   └── pagination.py
        │   │
        │   ├── domain_services/
        │   │   ├── ranking_service.py
        │   │   ├── facet_builder_service.py
        │   │   ├── query_normalization_service.py
        │   │   └── personalization_service.py
        │   │
        │   ├── policies/
        │   │   ├── freshness_policy.py
        │   │   ├── availability_policy.py
        │   │   ├── trust_boost_policy.py
        │   │   └── geo_boost_policy.py
        │   │
        │   └── exceptions/
        │       ├── invalid_query.py
        │       └── unsupported_filter.py
        │
        ├── application/
        │   ├── use_cases/
        │   │   ├── index_product/
        │   │   ├── update_index/
        │   │   ├── remove_from_index/
        │   │   ├── execute_search/
        │   │   └── rebuild_index/
        │   │
        │   ├── ports/
        │   │   ├── inbound/
        │   │   │   ├── search_query_port.py
        │   │   │   └── index_command_port.py
        │   │   │
        │   │   └── outbound/
        │   │       ├── search_engine_port.py
        │   │       ├── ranking_engine_port.py
        │   │       ├── analytics_port.py
        │   │       └── event_publisher_port.py
        │   │
        │   └── dto/
        │       ├── search_request_dto.py
        │       ├── search_result_dto.py
        │       └── facet_dto.py
        │
        ├── adapters/
        │   ├── inbound/
        │   │   ├── rest/
        │   │   │   ├── search_views.py
        │   │   │   ├── search_serializers.py
        │   │   │   └── search_urls.py
        │   │   │
        │   │   └── consumer/
        │   │       ├── product_events_handler.py
        │   │       ├── inventory_events_handler.py
        │   │       ├── pricing_events_handler.py
        │   │       ├── review_events_handler.py
        │   │       └── shipping_events_handler.py
        │   │
        │   └── outbound/
        │       ├── search_engines/
        │       │   ├── elasticsearch_adapter.py
        │       │   ├── opensearch_adapter.py
        │       │   └── meilisearch_adapter.py
        │       │
        │       ├── ranking/
        │       │   ├── rule_based_ranker.py
        │       │   ├── ml_ranker.py
        │       │   └── hybrid_ranker.py
        │       │
        │       └── cache/
        │           └── search_cache_adapter.py
        │
        ├── read_model/
        │   ├── indices/
        │   │   ├── product_search_index.json
        │   │   ├── suggestion_index.json
        │   │   └── category_index.json
        │   │
        │   ├── projections/
        │   │   ├── product_projection.py
        │   │   ├── availability_projection.py
        │   │   ├── pricing_projection.py
        │   │   ├── trust_projection.py
        │   │   └── geo_projection.py
        │   │
        │   └── rebuild/
        │       ├── rebuild_full_index.py
        │       └── replay_events_to_index.py
        │
        ├── saga/
        │   └── search_reindex_saga.py
        │
        ├── outbox/
        │   └── search_outbox_model.py
        │
        ├── tests/
        │   ├── relevance/
        │   ├── ranking/
        │   ├── indexing/
        │   └── adapters/
        │
        └── docs/
            ├── README.md
            ├── ranking.md
            ├── query_language.md
            ├── index_schema.md
            ├── failure_modes.md
            └── adr.md


🔁 EVENT → INDEX FLOW
ProductPublished
   ↓
Search Projection Builder
   ↓
Index Document Created
   ↓
Ranking Signals Attached
   ↓
Search Engine Index

📦 SEARCH DOCUMENT (REALISTIC)
{
  "product_id": "UUID",
  "title": "Wireless Earbuds",
  "description": "...",
  "price": 1299,
  "currency": "INR",
  "in_stock": true,
  "seller_score": 4.7,
  "review_count": 1823,
  "shipping_days": 2,
  "category_path": ["Electronics", "Audio"],
  "attributes": {
    "brand": "XYZ",
    "battery_life": "24h"
  },
  "boosts": {
    "freshness": 1.2,
    "trust": 1.4,
    "geo": 1.1
  }
}

🧮 RANKING SIGNALS (STAFF-LEVEL)
Signal	Source
Text relevance	Query match
Price competitiveness	Pricing
Availability	Inventory
Seller trust	Accounts
Reviews	Ratings
Shipping speed	Logistics
Personal history	Analytics

👉 Ranking ≠ sorting
👉 Ranking = behavior shaping

🔥 QUERY TYPES

Keyword search

Faceted search

Auto-suggestions

Category browse

Personalized feed

Trending products

🧬 DATABASE / INDEXES

Search uses:

Elasticsearch / OpenSearch

Redis (hot queries)

Analytics store (click-through)

No relational DB needed except:

rebuild tracking

index metadata

🚨 FAILURE MODES (DESIGNED)

Index lag → stale results tolerated

Search engine down → cached fallback

Bad ranking → rollback profile

Corrupt index → full rebuild

🧠 WHY THIS IS PRINCIPAL-LEVEL

Search is isolated

Ranking is explicit & testable

ML-ready but not ML-dependent

Fully rebuildable

Event-driven, not API-driven

🏁 YOU NOW HAVE:

✅ Products
✅ Orders
✅ Cart
✅ Inventory
✅ Checkout
✅ Shipping
✅ Coupons
✅ Accounts
✅ Notifications
✅ Search