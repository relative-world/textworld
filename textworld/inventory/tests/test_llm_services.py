import pytest
from textworld.inventory.llm_services import InventoryService
from textworld.inventory.models import Item

@pytest.fixture
def service():
    return InventoryService()

@pytest.fixture
def sample_item():
    return Item(
        id=1,
        name="Test Item",
        description="A test item",
        quantity=10,
        price=5.99,
        weight=1.5
    )

def test_create_inventory(service):
    result = service.create_inventory("Test Owner")
    assert "Inventory created for Test Owner with ID 1" in result
    assert len(service.store.inventories) == 1
    assert service.store.inventories[0].owner == "Test Owner"

def test_read_inventory_empty(service):
    service.create_inventory("Test Owner")
    result = service.read_inventory(1)
    assert "Inventory ID: 1" in result
    assert "Owner: Test Owner" in result
    assert "Items:" in result

def test_read_nonexistent_inventory(service):
    result = service.read_inventory(999)
    assert "not found" in result

def test_update_inventory(service):
    service.create_inventory("Old Owner")
    result = service.update_inventory(1, "New Owner")
    assert "updated with new owner New Owner" in result
    assert service.store.inventories[0].owner == "New Owner"

def test_update_nonexistent_inventory(service):
    result = service.update_inventory(999, "New Owner")
    assert "not found" in result

def test_delete_inventory(service):
    service.create_inventory("Test Owner")
    result = service.delete_inventory(1)
    assert "deleted" in result
    assert len(service.store.inventories) == 0

def test_delete_nonexistent_inventory(service):
    result = service.delete_inventory(999)
    assert "not found" in result

def test_add_item(service, sample_item):
    service.create_inventory("Test Owner")
    result = service.add_item(1, sample_item)
    assert "added to inventory" in result
    assert len(service.store.inventories[0].items) == 1

def test_add_item_to_nonexistent_inventory(service, sample_item):
    result = service.add_item(999, sample_item)
    assert "not found" in result

def test_remove_item(service, sample_item):
    service.create_inventory("Test Owner")
    service.add_item(1, sample_item)
    result = service.remove_item(1, 1)
    assert "removed from inventory" in result
    assert len(service.store.inventories[0].items) == 0

def test_remove_nonexistent_item(service):
    service.create_inventory("Test Owner")
    result = service.remove_item(1, 999)
    assert "not found" in result

def test_read_item(service, sample_item):
    service.create_inventory("Test Owner")
    service.add_item(1, sample_item)
    result = service.read_item(1, 1)
    assert "Test Item" in result
    assert "A test item" in result
    assert "10" in result
    assert "5.99" in result
    assert "1.5" in result

def test_read_nonexistent_item(service):
    service.create_inventory("Test Owner")
    result = service.read_item(1, 999)
    assert "not found" in result

def test_error_handling(service):
    # Test error handling by forcing an exception
    service.store = None
    result = service.create_inventory("Test Owner")
    assert "Error creating inventory" in result
