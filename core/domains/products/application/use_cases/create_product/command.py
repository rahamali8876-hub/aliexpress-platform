# command.py
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateProductCommand:
    """
    Command object for creating a Product aggregate.
    Matches the current minimal CreateProductHandler.
    """

    product_id: str
    seller_id: str
    title: str
