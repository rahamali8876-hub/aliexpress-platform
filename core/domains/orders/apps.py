from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'core.domains.orders'
    # verbose_name = 'Orders'
    label = "orders"   # IMPORTANT: unique short name
    
