docker compose exec api python manage.py makemigrations shared
docker compose exec api python manage.py migrate

docker compose exec api python manage.py makemigrations products
docker compose exec api python manage.py migrate

{
  "seller_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Wireless Mouse",
  "price": 15.99,
  "stock": 100
}

### get into perticular service shell

    # Product Kafka consumer
    docker compose exec api python manage.py run_product_event_consumer

    # Outbox
    docker compose exec api python manage.py process_outbox

docker compose exec api python manage.py process_outbox
docker exec -it aliexpress_kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list


docker exec -it aliexpress_kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic product.created \
  --from-beginning


docker exec -it aliexpress_kafka \
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic product.events \
--from-beginning





###  THE CANONICAL EVENT FLOW (LOCK THIS IN YOUR HEAD)
  DOMAIN
    ↓
  OutboxEvent (DB)
    ↓
  OutboxProcessor (infra)
    ↓
  Event Envelope (infra)
    ↓
  Kafka Topic (domain-level)
    ↓
  Consumer (adapter)
    ↓
  Projection / Side Effect