# # # # filename : core/domains/products/management/commands/rebuild_product_search_projection.py

from django.core.management.base import BaseCommand
from core.domains.products.read_model.repositories.product_search_repository import (
    ProductSearchRepository,
)
from core.domains.products.read_model.documents.product_search_document import (
    ProductSearchDocument,
)

from core.domains.products.adapters.outbound.persistence.models.product_model import (
    ProductModel,
)

from core.shared.infrastructure.search.elasticsearch_client import get_es_client


class Command(BaseCommand):
    help = "Rebuild product search projection from database"

    def handle(self, *args, **options):
        es = get_es_client()
        repo = ProductSearchRepository()

        self.stdout.write("Rebuilding product search projection...")

        for product in ProductModel.objects.iterator():
            document = ProductSearchDocument(
                id=str(product.id),
                title=product.title,
                seller_id=str(product.seller_id),
                price=product.price,
                status=product.status,
                occurred_at=product.created_at,
            )

            es.index(
                index=repo.INDEX_ALIAS,
                id=document.id,
                document=document.to_dict(),
            )

        self.stdout.write(self.style.SUCCESS("Projection rebuild complete"))
