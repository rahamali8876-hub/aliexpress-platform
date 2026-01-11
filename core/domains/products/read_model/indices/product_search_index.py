# # filename : core/domains/products/read_model/indices/product_search_index.py

import logging

logging.debug(
    "Product Search Index : "
    "core/domains/products/read_model/indices/product_search_index.py"
)
PRODUCT_SEARCH_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "text"},
            "price": {"type": "float"},
            "occurred_at": {"type": "date"},
        }
    }
}
