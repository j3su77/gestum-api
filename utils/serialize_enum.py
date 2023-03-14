
from enum import Enum
def serialize_enum(obj):
    return obj.value if isinstance(obj, Enum) else None
