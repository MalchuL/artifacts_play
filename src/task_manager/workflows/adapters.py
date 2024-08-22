from typing import List, Optional
from pydantic import TypeAdapter

from src.playground.items import Items, Item

ItemsAdapter = TypeAdapter(Optional[Items])
ListItemsAdapter = TypeAdapter(Optional[List[Items]])
ListItemAdapter = TypeAdapter(Optional[List[Item]])


def from_json(obj, adapter):
    return adapter.validator.validate_python(obj)


def to_json(obj, adapter):
    return adapter.dump_python(obj)
