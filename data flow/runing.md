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


error to solve 
python manage.py run_product_consumer

06
ikali ➜ /workspaces/aliexpress-platform (master) $ docker compose exec api python manage.py process_outbox
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
WARN[0000] The "b" variable is not set. Defaulting to a blank string. 
Traceback (most recent call last):
  File "/app/manage.py", line 50, in <module>
    main()
  File "/app/manage.py", line 46, in main
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 443, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 437, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 276, in fetch_command
    klass = load_command_class(app_name, subcommand)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/core/management/__init__.py", line 48, in load_command_class
    module = import_module("%s.management.commands.%s" % (app_name, name))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/app/core/shared/management/commands/process_outbox.py", line 21, in <module>
    from core.shared.infrastructure.messaging.outbox_publisher import OutboxPublisher
  File "/app/core/shared/infrastructure/messaging/outbox_publisher.py", line 12, in <module>
    from core.shared.observability.metrics.prometheus import (
ModuleNotFoundError: No module named 'core.shared.observability.metrics.prometheus'
@Rofikali ➜ /workspaces/aliexpress-platform (master) $ 