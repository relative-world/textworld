from typing import Annotated
from pydantic import BaseModel, Field
from textworld.inventory.models import Inventory, Item

class InventoryStore(BaseModel):
    inventories: Annotated[list[Inventory], Field(default_factory=list)]

    def add_inventory(self, inventory: Inventory) -> None:
        self.inventories.append(inventory)

    def remove_inventory(self, inventory_id: int) -> bool:
        for inventory in self.inventories:
            if inventory.id == inventory_id:
                self.inventories.remove(inventory)
                return True
        return False

    def get_inventory(self, inventory_id: int) -> Inventory | None:
        for inventory in self.inventories:
            if inventory.id == inventory_id:
                return inventory
        return None

    def add_item_to_inventory(self, inventory_id: int, item: Item) -> bool:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            inventory.items.append(item)
            return True
        return False

    def remove_item_from_inventory(self, inventory_id: int, item_id: int) -> bool:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            for item in inventory.items:
                if item.id == item_id:
                    inventory.items.remove(item)
                    return True
        return False

    def get_item_from_inventory(self, inventory_id: int, item_id: int) -> Item | None:
        inventory = self.get_inventory(inventory_id)
        if inventory:
            for item in inventory.items:
                if item.id == item_id:
                    return item
        return None

