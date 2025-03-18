from utilities import cache
import pytest

MAX_SIZE: int = 100
TTL: int = 60
ENTRIES: list[cache.Entry] = [cache.Entry(f"{i:0>3d}") for i in range(10)]

@pytest.fixture
def cache_fixtures():
    c = cache.Cache(max_size=MAX_SIZE, ttl=TTL)
    [c.set(str(i), i) for i in ENTRIES]
    return c

def test_cache_initialization(cache_fixtures: cache.Cache):
    c = cache_fixtures
    assert c.max_size == MAX_SIZE
    assert c.ttl == TTL
