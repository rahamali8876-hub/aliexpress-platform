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
docker compose exec api python manage.py run_product_event_consumer
docker compose exec api python manage.py run_product_consumer

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

docker exec -it aliexpress_kafka \
kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic product.created \
--from-beginning


error to solve **************************************************************
┌──────────────┐
│  Django API  │
│              │
│ ✔ Creates product
│ ✔ Inserts OutboxEvent
│ ✔ status = PENDING
│ ✔ DB commit happens
│
│ ❌ PROBLEM NOT HERE
└──────┬───────┘
       │ DB TX (atomic)
       │
       │ ⚠ If Kafka was here → would be WRONG
       ▼
┌──────────────────────┐
│   OutboxEvent Table  │
│                      │
│ ✔ Events exist
│ ✔ status = PENDING
│ ✔ retry_count = 0
│ ✔ visible in admin
│
│ ❌ PROBLEM #1:
│ Events are NOT marked
│ PUBLISHED after send
│ OR ownership logic
│ was broken earlier
│
│ ❌ PROBLEM #2:
│ Multiple runs re-pick
│ same PENDING rows
└──────┬───────────────┘
       │ poll
       │
       │ ⚠ select_for_update
       │ ⚠ skip_locked
       │
       │ ❌ Earlier version:
       │   No PROCESSING state
       │   → duplicate publish
       ▼
┌──────────────────────┐
│  OutboxPublisher     │
│  (Kafka Producer)   │
│                      │
│ ✔ Kafka send works
│ ✔ Messages appear
│   in Kafka UI (+50)
│
│ ❌ PROBLEM #3:
│ Kafka ACK received
│ BUT DB row not safely
│ updated to PUBLISHED
│
│ ❌ PROBLEM #4:
│ Two _process_event()
│ versions existed
│ → wrong method called
│ → state not updated
└──────┬───────────────┘
       │ send
       │
       │ ✔ producer.send()
       │ ✔ future.get()
       ▼
┌──────────────────────┐
│   Kafka Topic        │
│ product.created     │
│                      │
│ ✔ Message count grows
│ ✔ Partition = 1
│ ✔ Offset increases
│
│ ❌ CONFUSION HERE:
│ UI shows messages
│ but consumer sees 0
│
│ ❌ CAUSE:
│ Consumer group offset
│ already at latest
│ OR wrong topic
│ OR different group.id
└──────┬───────────────┘
       │ poll
       │
       │ ❌ Consumer started
       │ but no new messages
       ▼
┌──────────────────────┐
│ Consumer Group       │
│ product-consumer     │
│                      │
│ ✔ Process is running
│ ✔ Poll loop active
│
│ ❌ PROBLEM #5:
│ Offsets already
│ committed
│
│ ❌ You used:
│ --from-beginning
│ only in console,
│ NOT in real consumer
└──────┬───────────────┘
       │
       │ ❌ No processing
       ▼
┌──────────────────────┐
│ Business Logic       │
│                      │
│ ❌ Never executed
│ ❌ Looks "broken"
│ ❌ Actually consumer
│     never received
│     events
└──────────────────────┘

docker exec -it aliexpress_kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group product-consumer \
  --describe
