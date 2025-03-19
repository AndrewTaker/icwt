import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entry:
    value: Any
    timestamp: int = field(init=False)

    def __post_init__(self):
        self.timestamp = int(time.time())


class Cache:
    def __init__(self, max_size: int, ttl: int):
        self.cache: OrderedDict[str, Entry] = OrderedDict()
        self.max_size: int = max_size
        self.ttl: int = ttl

    def get(self, key: str):
        if key in self.cache:
            entry = self.cache[key]
            if int(time.time()) - entry.timestamp < self.ttl:
                self.cache.move_to_end(key)
                return entry.value
            del self.cache[key]
        return None

    def set(self, key: str, entry: Entry):
        self._cleanup()

        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        entry.timestamp = int(time.time())
        self.cache[key] = entry

    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()

    def _cleanup(self):
        current_time = int(time.time())
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time - entry.timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]

# def qq():
#     c = Cache(5, 2)
#     e = Entry([1,2,])
#     for i in range(30):
#         c.set("qq", e)
#         c.get("qq")
#         if i == 10 or i == 15:
#             c.set("qq", Entry([1,2,3,4,5]))
#         print(i, c.cache)
#         time.sleep(1)
#
# qq()
