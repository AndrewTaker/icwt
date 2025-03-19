from app.utilities.cache import Cache, Entry
import pytest

MAX_SIZE: int = 5
TTL: int = 60
ENTRIES: list[Entry] = [Entry(f"{i:0>3d}") for i in range(MAX_SIZE)]

@pytest.fixture
def cache_fixtures() -> Cache:
    c = Cache(max_size=MAX_SIZE, ttl=TTL)
    [c.set(str(i.value), i) for i in ENTRIES]
    return c

def test_cache_initialization(cache_fixtures: Cache):
    c = cache_fixtures
    assert c.max_size == MAX_SIZE
    assert c.ttl == TTL

def test_cache_getter(cache_fixtures: Cache):
    c = cache_fixtures
    assert c.get("non existing key") == None
    assert c.get("001") == "001"

def test_cache_setter(cache_fixtures: Cache):
    c = cache_fixtures
    c.set("test_string_value", Entry("test_value"))
    c.set("test_integer_value", Entry(123))
    c.set("test_list_value", Entry([1, 2, 3]))
    c.set("test_dictionary_value", Entry({"1": 1, "2": 2}))
    assert c.get("test_string_value") == "test_value"
    assert c.get("test_integer_value") == 123
    assert c.get("test_list_value") == [1, 2, 3]
    assert c.get("test_dictionary_value") == {"1": 1, "2": 2}

def test_cache_deleter(cache_fixtures: Cache):
    c = cache_fixtures
    c.delete("001")
    assert c.get("001") == None
    assert c.delete("non existing key") is None

def test_cache_clearer(cache_fixtures: Cache):
    c = cache_fixtures
    c.clear()
    assert len(c.cache) == 0

def test_cache_fifo(cache_fixtures: Cache):
    c = cache_fixtures
    assert len(c.cache) == MAX_SIZE
    c.set("new key", Entry(123))
    assert c.get("000") is None
