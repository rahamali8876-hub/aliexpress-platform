from core.shared.kernel.domain_event import DomainEvent


class ProductCreated(DomainEvent):
    event_type = "product.created"
