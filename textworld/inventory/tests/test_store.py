import pytest
from textworld.inventory.store import InventoryStore
from textworld.inventory.models import Inventory, Item

@pytest.fixture
def store():
    return InventoryStore()

@pytest.fixture
def sample_inventory():
    return Inventory(id=1, name="Test Inventory", items=[], owner="Test Owner")

@pytest.fixture
def sample_item():
    return Item(id=1, name="Test Item", description="A test item", quantity=10, price=5.99, weight=1.5)

def test_add_inventory(store, sample_inventory):
    store.add_inventory(sample_inventory)
    assert len(store.inventories) == 1
    assert store.inventories[0] == sample_inventory

def test_remove_inventory(store, sample_inventory):
    store.add_inventory(sample_inventory)
    result = store.remove_inventory(1)
    assert result is True
    assert len(store.inventories) == 0

def test_remove_nonexistent_inventory(store):
    result = store.remove_inventory(999)
    assert result is False

def test_get_inventory(store, sample_inventory):
    store.add_inventory(sample_inventory)
    result = store.get_inventory(1)
    assert result == sample_inventory

def test_get_nonexistent_inventory(store):
    result = store.get_inventory(999)
    assert result is None

def test_add_item_to_inventory(store, sample_inventory, sample_item):
    store.add_inventory(sample_inventory)
    result = store.add_item_to_inventory(1, sample_item)
    assert result is True
    assert len(store.get_inventory(1).items) == 1
    assert store.get_inventory(1).items[0] == sample_item

def test_add_item_to_nonexistent_inventory(store, sample_item):
    result = store.add_item_to_inventory(999, sample_item)
    assert result is False

def test_remove_item_from_inventory(store, sample_inventory, sample_item):
    store.add_inventory(sample_inventory)
    store.add_item_to_inventory(1, sample_item)
    result = store.remove_item_from_inventory(1, 1)
    assert result is True
    assert len(store.get_inventory(1).items) == 0

def test_remove_nonexistent_item_from_inventory(store, sample_inventory):
    store.add_inventory(sample_inventory)
    result = store.remove_item_from_inventory(1, 999)
    assert result is False

def test_get_item_from_inventory(store, sample_inventory, sample_item):
    store.add_inventory(sample_inventory)
    store.add_item_to_inventory(1, sample_item)
    result = store.get_item_from_inventory(1, 1)
    assert result == sample_item

def test_get_nonexistent_item_from_inventory(store, sample_inventory):
    store.add_inventory(sample_inventory)
    result = store.get_item_from_inventory(1, 999)
    assert result is None
