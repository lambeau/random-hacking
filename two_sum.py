import random

items = [random.randint(-50, 50) for i in range(100)]
expected = 27

print(items)

seen = set()

for i in items:
    if expected - i in seen:
        print(i, expected - i)
    seen.add(i)

print(seen)
