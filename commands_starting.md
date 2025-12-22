### docker compose exec api python manage.py process_outbox

### docker compose exec api python manage.py run_inventory_consumer

### # API 
    docker compose up

    # Outbox
    docker compose exec api python manage.py process_outbox

    # Inventory consumer
    docker compose exec api python manage.py run_inventory_consumer

    # Checkout saga
    docker compose exec api python manage.py run_checkout_saga
