from utilities import cache
import pytest

MAX_SIZE: int = 100
TTL: int = 60
ENTRIES: list[cache.Entry] = [cache.Entry(f"{i:0>3d}") for i in range(10)]

@pytest.fixture
def cache_fixtures():
    c = cache.Cache(max_size=MAX_SIZE, ttl=TTL)
    [c.set(str(i.value), i) for i in ENTRIES]
    c.p()
    return c

def test_cache_initialization(cache_fixtures: cache.Cache):
    c = cache_fixtures
    assert c.max_size == MAX_SIZE
    assert c.ttl == TTL

def test_cache_getter(cache_fixtures: cache.Cache):
    c = cache_fixtures
    assert c.get("non existing key") == None
    assert c.get("001") == "001"

def test_cache_setter(cache_fixtures: cache.Cache):
    c = cache_fixtures
    c.set("test_string_value", cache.Entry("test_value"))
    c.set("test_integer_value", cache.Entry(123))
    c.set("test_list_value", cache.Entry([1, 2, 3]))
    c.set("test_dictionary_value", cache.Entry({"1": 1, "2": 2}))
    assert c.get("test_string_value") == "test_value"
    assert c.get("test_integer_value") == 123
    assert c.get("test_list_value") == [1, 2, 3]
    assert c.get("test_dictionary_value") == {"1": 1, "2": 2}

