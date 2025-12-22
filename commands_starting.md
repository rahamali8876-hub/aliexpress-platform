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



### 3️⃣ Correct structure (Principal-level DDD + Django-friendly)

For each use case, the folder should look like this:

core/domains/products/application/use_cases/create_product/
├── __init__.py
├── command.py         # defines CreateProductCommand
├── handler.py         # defines CreateProductHandler
├── validator.py       # optional
├── mapper.py          # optional
└── events.py          # optional


Then for update_product:

core/domains/products/application/use_cases/update_product/
├── __init__.py
├── command.py         # defines UpdateProductCommand
├── handler.py         # defines UpdateProductHandler
└── ...


This makes every use case a proper Python package, and allows absolute imports.