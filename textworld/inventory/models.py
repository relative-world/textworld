from typing import Annotated
from pydantic import BaseModel, Field

class Item(BaseModel):
    id: Annotated[int, Field(...)]
    name: Annotated[str, Field(...)]
    description: Annotated[str | None, Field(None)]
    quantity: Annotated[int, Field(...)]
    price: Annotated[float, Field(...)]
    weight: Annotated[float | None, Field(None)]

class Inventory(BaseModel):
    id: Annotated[int, Field(...)]
    owner: Annotated[str, Field(...)]
    items: Annotated[list[Item], Field(default_factory=list)]
