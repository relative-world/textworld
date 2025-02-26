from textworld.inventory.models import Inventory, Item
from textworld.inventory.store import InventoryStore

class InventoryService:
    def __init__(self):
        self.store = InventoryStore()

    def create_inventory(self, owner: str) -> str:
        try:
            new_inventory = Inventory(id=len(self.store.inventories) + 1, owner=owner)
            self.store.add_inventory(new_inventory)
            return f"Inventory created for {owner} with ID {new_inventory.id}."
        except Exception as e:
            return f"Error creating inventory: {str(e)}"

    def read_inventory(self, inventory_id: int) -> str:
        try:
            inventory = self.store.get_inventory(inventory_id)
            if inventory:
                items = "\n".join([f"{item.quantity}x {item.name} (ID: {item.id})" for item in inventory.items])
                return f"Inventory ID: {inventory.id}\nOwner: {inventory.owner}\nItems:\n{items}"
            return f"Inventory with ID {inventory_id} not found."
        except Exception as e:
            return f"Error reading inventory: {str(e)}"

    def update_inventory(self, inventory_id: int, owner: str) -> str:
        try:
            inventory = self.store.get_inventory(inventory_id)
            if inventory:
                inventory.owner = owner
                return f"Inventory ID {inventory_id} updated with new owner {owner}."
            return f"Inventory with ID {inventory_id} not found."
        except Exception as e:
            return f"Error updating inventory: {str(e)}"

    def delete_inventory(self, inventory_id: int) -> str:
        try:
            if self.store.remove_inventory(inventory_id):
                return f"Inventory with ID {inventory_id} deleted."
            return f"Inventory with ID {inventory_id} not found."
        except Exception as e:
            return f"Error deleting inventory: {str(e)}"

    def add_item(self, inventory_id: int, item: Item) -> str:
        try:
            if self.store.add_item_to_inventory(inventory_id, item):
                return f"Item {item.name} added to inventory ID {inventory_id}."
            return f"Inventory with ID {inventory_id} not found."
        except Exception as e:
            return f"Error adding item: {str(e)}"

    def remove_item(self, inventory_id: int, item_id: int) -> str:
        try:
            if self.store.remove_item_from_inventory(inventory_id, item_id):
                return f"Item with ID {item_id} removed from inventory ID {inventory_id}."
            return f"Item with ID {item_id} not found in inventory ID {inventory_id}."
        except Exception as e:
            return f"Error removing item: {str(e)}"

    def read_item(self, inventory_id: int, item_id: int) -> str:
        try:
            item = self.store.get_item_from_inventory(inventory_id, item_id)
            if item:
                return (f"Item ID: {item.id}\nName: {item.name}\nDescription: {item.description}\n"
                        f"Quantity: {item.quantity}\nPrice: {item.price}\nWeight: {item.weight}")
            return f"Item with ID {item_id} not found in inventory ID {inventory_id}."
        except Exception as e:
            return f"Error reading item: {str(e)}"
