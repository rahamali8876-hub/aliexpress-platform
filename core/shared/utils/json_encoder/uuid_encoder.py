# # core/shared/utils/json_encoder/uuid_encoder.py

# import json
# import uuid
# from datetime import datetime, date
# from decimal import Decimal


# class CustomJSONEncoder(json.JSONEncoder):
#     """
#     Staff-level JSON encoder that handles:
#       - UUID
#       - datetime / date
#       - Decimal
#     """

#     def default(self, obj):
#         if isinstance(obj, uuid.UUID):
#             return str(obj)
#         if isinstance(obj, (datetime, date)):
#             return obj.isoformat()
#         if isinstance(obj, Decimal):
#             return float(obj)
#         return super().default(obj)


# def dumps(data: dict, **kwargs) -> str:
#     """Convert dict to JSON string using the custom encoder"""
#     return json.dumps(data, cls=CustomJSONEncoder, **kwargs)


# def loads(data: str, **kwargs) -> dict:
#     """Parse JSON string back to dict"""
#     return json.loads(data, **kwargs)




# filename : core/shared/utils/json_encoder/uuid_encoder.py

