# file name: core/domains/products/adapters/inbound/rest/product_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.domains.products.application.use_cases.create_product.command import (
    CreateProductCommand,
)
from core.domains.products.application.use_cases.create_product.handler import (
    CreateProductHandler,
)
from core.domains.products.adapters.outbound.persistence.product_repository_impl import (
    ProductRepositoryImpl,
)
from core.domains.products.adapters.outbound.messaging.product_event_publisher import (
    ProductEventPublisher,
)
from core.domains.products.adapters.inbound.rest.product_serializer import (
    CreateProductSerializer,
)


class CreateProductView(APIView):
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        handler = CreateProductHandler(
            repository=ProductRepositoryImpl(),
        )

        command = CreateProductCommand(**serializer.validated_data)
        aggregate = handler.handle(command)

        return Response(
            {"product_id": str(aggregate.product_id)},
            status=status.HTTP_201_CREATED,
        )
