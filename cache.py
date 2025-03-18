import time
from dataclasses import dataclass
from typing import Any

@dataclass
class Entry:
    value: Any
    timestamp: int = int(time.time())

class Cache:
    def __init__(self, max_size: int, ttl: int):
        self.cache: dict[str, Entry] = {}
        self.max_size: int = max_size
        self.ttl: int = ttl

    def get(self, key: str):
        if key in self.cache:
            entry = self.cache[key]
            if int(time.time()) - entry.timestamp < self.ttl:
                return entry.value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, entry: Entry):
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = entry

    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()
