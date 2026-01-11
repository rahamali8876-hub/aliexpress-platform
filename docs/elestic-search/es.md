### 🧱 ROUTE → QUERY FLOW (STAFF GRADE)

    HTTP Route
    ↓
    Query Handler (Application layer)
    ↓
    Search Repository (Port)
    ↓
    Elasticsearch Adapter
    ↓
    Alias (product_search_current)
    ↓
    Actual Index (v1_xxx / v1_yyy)

### 🧱 DETAILED FLOW

    HTTP GET /products/search/
    ↓
    ProductSearchViewSet
    ↓
    SearchProductsQuery (application)
    ↓
    ProductSearchPort (interface)
    ↓
    Elasticsearch Adapter
    ↓
    Alias: product_search_current
    ↓
    Index: product_search_v1_xxxx



uv run ./scripts/post_products_data.py 
docker compose exec api python manage.py process_outbox
docker compose exec api python manage.py run_product_event_consumer
docker compose exec api python manage.py run_product_consumer


### curl -X PUT http://127.0.0.1:9200/products_v1 \
-H "Content-Type: application/json" \
  -d '{
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    },
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "id": { "type": "keyword" },
        "title": {
          "type": "text",
          "analyzer": "standard",
          "fields": {
            "keyword": { "type": "keyword" }
          }
        },
        "seller_id": { "type": "keyword" },
        "price": { "type": "double" },
        "status": { "type": "keyword" },
        "occurred_at": { "type": "date" }
      }
    }
  }'



### curl -X GET http://127.0.0.1:9200/_cat/indices?v

curl -X POST http://127.0.0.1:9200/_aliases \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "add": {
          "index": "products_v1",
          "alias": "products_search"
        }
      }
    ]
  }'

  
