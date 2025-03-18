from utilities import cache

c = cache.Cache(100, 10)
c.set("qq", cache.Entry("qweqwe"))
print(c.get("qq"))
