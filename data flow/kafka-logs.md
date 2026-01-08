docker exec -it aliexpress_kafka kafka-broker-api-versions \
  --bootstrap-server localhost:9092

docker exec -it aliexpress_kafka kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --list

docker exec -it aliexpress_kafka product-command-consumer-group   --bootstrap-server kafka:9092   --group product-event-projection-group   --describe
docker exec -it aliexpress_kafka product-event-projection-group   --bootstrap-server kafka:9092   --group product-event-projection-group   --describe

docker exec -it aliexpress_kafka kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --group product-consumer \
  --describe



docker exec -it aliexpress_kafka kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --describe \
  --group product-consumer

docker exec -it aliexpress_kafka kafka-consumer-groups \
  --bootstrap-server aliexpress_kafka:9092 \
  --describe \
  --group product-consumer-group



docker compose exec api python manage.py process_outbox
docker compose exec api python manage.py run_product_consumer
docker compose exec api python manage.py run_product_event_consumer

docker exec -it aliexpress_kafka \
kafka-consumer-groups \
--bootstrap-server aliexpress_kafka:9092 \
--group product-event-projection-group \
--describe
