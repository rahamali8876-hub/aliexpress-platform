# filename : core/domains/products/read_model/repositories/product_search_repository.py

import logging
from typing import Optional, List
from core.shared.infrastructure.search.elasticsearch_client import get_es_client


class ProductSearchRepository:
    logging.debug("ProductSearchRepository initialized.")
    INDEX_ALIAS = "products_search"

    def search(
        self,
        *,
        title: Optional[str],
        min_price: Optional[float],
        max_price: Optional[float],
    ) -> List[dict]:
        must = []
        filter_ = []

        if title:
            # must.append({"match": {"name": {"query": title, "operator": "and"}}})
            must.append({"match": {"title": {"query": title, "operator": "and"}}})

        if min_price is not None or max_price is not None:
            price_filter = {}
            if min_price is not None:
                price_filter["gte"] = min_price
            if max_price is not None:
                price_filter["lte"] = max_price

            filter_.append({"range": {"price": price_filter}})

        # query = {
        #     "bool": {
        #         "must": must if must else [{"match_all": {}}],
        #         "filter": filter_,
        #     }
        # }
        query = {
            "bool": {
                "must": must or [{"match_all": {}}],
                "filter": filter_,
            }
        }

        response = get_es_client().search(
            index=self.INDEX_ALIAS,
            query=query,
        )

        return [hit["_source"] for hit in response["hits"]["hits"]]
