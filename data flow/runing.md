### docker compose logs -f api ( Django app logs )

    Postgres is up!
    Applying migrations...
    Starting gunicorn...

### docker compose up ( start all services )

    docker compose \
    -f docker-compose.yml \
    -f docker-compose.observability.yml \
    up -d

### get into perticular service shell

    # Product Kafka consumer
    docker compose exec api python manage.py run_product_event_consumer

    # Outbox
    docker compose exec api python manage.py process_outbox

docker compose exec api python manage.py makemigrations shared
docker compose exec api python manage.py migrate


docker exec -it aliexpress_kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic product.created \
  --from-beginning
