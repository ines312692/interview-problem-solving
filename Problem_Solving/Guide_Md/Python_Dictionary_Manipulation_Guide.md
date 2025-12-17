# Python Dictionary Manipulation Guide

A comprehensive reference for working with dictionaries in Python.

---

## Table of Contents

1. [Creating Dictionaries](#creating-dictionaries)
2. [Accessing Values](#accessing-values)
3. [Adding & Updating Elements](#adding--updating-elements)
4. [Removing Elements](#removing-elements)
5. [Checking Keys & Values](#checking-keys--values)
6. [Iterating Over Dictionaries](#iterating-over-dictionaries)
7. [Dictionary Methods](#dictionary-methods)
8. [Merging Dictionaries](#merging-dictionaries)
9. [Copying Dictionaries](#copying-dictionaries)
10. [Dictionary Comprehensions](#dictionary-comprehensions)
11. [Nested Dictionaries](#nested-dictionaries)
12. [Sorting Dictionaries](#sorting-dictionaries)
13. [Default Values & DefaultDict](#default-values--defaultdict)
14. [Counter & OrderedDict](#counter--ordereddict)
15. [Useful Patterns & Tricks](#useful-patterns--tricks)
16. [Key Differences to Remember](#key-differences-to-remember)

---

## Creating Dictionaries

```python
# Empty dictionary
my_dict = {}
my_dict = dict()

# With key-value pairs
person = {"name": "Alice", "age": 30, "city": "Paris"}

# Using dict() constructor
person = dict(name="Alice", age=30, city="Paris")

# From list of tuples
pairs = [("a", 1), ("b", 2), ("c", 3)]
my_dict = dict(pairs)  # {'a': 1, 'b': 2, 'c': 3}

# From two lists with zip
keys = ["name", "age", "city"]
values = ["Alice", 30, "Paris"]
my_dict = dict(zip(keys, values))

# Using fromkeys() - same value for all keys
keys = ["a", "b", "c"]
my_dict = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}
my_dict = dict.fromkeys(keys)     # {'a': None, 'b': None, 'c': None}

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

---

## Accessing Values

```python
person = {"name": "Alice", "age": 30, "city": "Paris"}

# Direct access with [] - raises KeyError if key doesn't exist
person["name"]           # "Alice"
person["country"]        # KeyError!

# Safe access with get() - returns None or default if key doesn't exist
person.get("name")       # "Alice"
person.get("country")    # None
person.get("country", "Unknown")  # "Unknown" (custom default)

# Get all keys, values, or items
person.keys()            # dict_keys(['name', 'age', 'city'])
person.values()          # dict_values(['Alice', 30, 'Paris'])
person.items()           # dict_items([('name', 'Alice'), ('age', 30), ('city', 'Paris')])

# Convert to lists
list(person.keys())      # ['name', 'age', 'city']
list(person.values())    # ['Alice', 30, 'Paris']
list(person.items())     # [('name', 'Alice'), ('age', 30), ('city', 'Paris')]
```

---

## Adding & Updating Elements

```python
person = {"name": "Alice", "age": 30}

# Add or update single key
person["city"] = "Paris"         # Add new key
person["age"] = 31               # Update existing key

# update() - Add/update multiple keys
person.update({"country": "France", "age": 32})
person.update(job="Engineer")    # Using keyword arguments

# setdefault() - Set value only if key doesn't exist
person.setdefault("name", "Bob")     # Returns "Alice" (key exists, no change)
person.setdefault("email", "a@b.com") # Adds key, returns "a@b.com"

# Merge with | operator (Python 3.9+)
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = dict1 | dict2           # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# In-place merge with |= (Python 3.9+)
dict1 |= dict2                   # dict1 is now merged
```

---

## Removing Elements

```python
person = {"name": "Alice", "age": 30, "city": "Paris", "country": "France"}

# pop() - Remove and return value by key
age = person.pop("age")          # Returns 30, key removed
val = person.pop("unknown", "default")  # Returns "default" if key doesn't exist

# popitem() - Remove and return last inserted key-value pair
last = person.popitem()          # Returns ('country', 'France')

# del - Delete by key
del person["city"]               # Removes 'city' key

# clear() - Remove all elements
person.clear()                   # person = {}

# Remove key if exists (safe deletion)
person.pop("unknown", None)      # No error if key doesn't exist
```

---

## Checking Keys & Values

```python
person = {"name": "Alice", "age": 30, "city": "Paris"}

# Check if key exists
"name" in person                 # True
"country" in person              # False
"country" not in person          # True

# Check if value exists
"Alice" in person.values()       # True
30 in person.values()            # True

# Check if key-value pair exists
("name", "Alice") in person.items()  # True

# Get number of items
len(person)                      # 3
```

---

## Iterating Over Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "Paris"}

# Iterate over keys (default)
for key in person:
    print(key)
# name, age, city

# Explicitly iterate over keys
for key in person.keys():
    print(key)

# Iterate over values
for value in person.values():
    print(value)
# Alice, 30, Paris

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
# name: Alice
# age: 30
# city: Paris

# With enumerate (get index)
for index, (key, value) in enumerate(person.items()):
    print(f"{index}. {key}: {value}")
```

---

## Dictionary Methods

```python
d = {"a": 1, "b": 2, "c": 3}

# All methods summary
d.keys()              # View of all keys
d.values()            # View of all values
d.items()             # View of all (key, value) pairs
d.get(key, default)   # Get value or default
d.setdefault(key, default)  # Get value or set & return default
d.pop(key, default)   # Remove & return value
d.popitem()           # Remove & return last item
d.update(other)       # Update with other dict or key-value pairs
d.clear()             # Remove all items
d.copy()              # Shallow copy
dict.fromkeys(keys, value)  # Create dict from keys with same value
```

---

## Merging Dictionaries

```python
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}  # Note: 'b' exists in both

# Method 1: | operator (Python 3.9+) - creates new dict
merged = dict1 | dict2   # {'a': 1, 'b': 3, 'c': 4}
# Right dict wins on conflicts

# Method 2: |= operator (Python 3.9+) - in-place update
dict1 |= dict2           # dict1 = {'a': 1, 'b': 3, 'c': 4}

# Method 3: update() - in-place
dict1 = {"a": 1, "b": 2}
dict1.update(dict2)      # dict1 = {'a': 1, 'b': 3, 'c': 4}

# Method 4: ** unpacking - creates new dict
merged = {**dict1, **dict2}  # {'a': 1, 'b': 3, 'c': 4}

# Method 5: dict() with ** unpacking
merged = dict(**dict1, **dict2)  # Only works with string keys

# Merge multiple dictionaries
dict1 = {"a": 1}
dict2 = {"b": 2}
dict3 = {"c": 3}
merged = {**dict1, **dict2, **dict3}  # {'a': 1, 'b': 2, 'c': 3}
merged = dict1 | dict2 | dict3        # Python 3.9+
```

---

## Copying Dictionaries

```python
original = {"name": "Alice", "scores": [90, 85, 88]}

# Shallow copy methods (nested objects share references)
copy1 = original.copy()
copy2 = dict(original)
copy3 = {**original}

# Deep copy (completely independent copy)
import copy
deep = copy.deepcopy(original)

# Demonstration of shallow vs deep copy
original["scores"].append(95)
print(copy1["scores"])    # [90, 85, 88, 95] (affected!)
print(deep["scores"])     # [90, 85, 88] (not affected)
```

---

## Dictionary Comprehensions

```python
# Basic syntax: {key_expr: value_expr for item in iterable}
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# With condition (filter)
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Transform existing dictionary
prices = {"apple": 1.0, "banana": 0.5, "orange": 0.75}
discounted = {k: v * 0.9 for k, v in prices.items()}
# {'apple': 0.9, 'banana': 0.45, 'orange': 0.675}

# Filter dictionary
expensive = {k: v for k, v in prices.items() if v > 0.6}
# {'apple': 1.0, 'orange': 0.75}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# From two lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
# {'a': 1, 'b': 2, 'c': 3}

# Conditional value
numbers = [1, 2, 3, 4, 5]
d = {n: "even" if n % 2 == 0 else "odd" for n in numbers}
# {1: 'odd', 2: 'even', 3: 'odd', 4: 'even', 5: 'odd'}

# Nested comprehension (flatten)
nested = {"a": {"x": 1, "y": 2}, "b": {"x": 3, "y": 4}}
flat = {f"{outer}_{inner}": val 
        for outer, inner_dict in nested.items() 
        for inner, val in inner_dict.items()}
# {'a_x': 1, 'a_y': 2, 'b_x': 3, 'b_y': 4}
```

---

## Nested Dictionaries

```python
# Creating nested dictionaries
users = {
    "alice": {
        "age": 30,
        "email": "alice@example.com",
        "scores": [90, 85, 88]
    },
    "bob": {
        "age": 25,
        "email": "bob@example.com",
        "scores": [75, 80, 82]
    }
}

# Accessing nested values
users["alice"]["age"]           # 30
users["alice"]["scores"][0]     # 90

# Safe access for nested keys
users.get("alice", {}).get("age")        # 30
users.get("charlie", {}).get("age")      # None (no error)

# Adding nested values
users["alice"]["city"] = "Paris"
users["charlie"] = {"age": 35}

# Updating nested values
users["alice"]["scores"].append(92)

# Iterating nested dictionaries
for username, info in users.items():
    print(f"{username}:")
    for key, value in info.items():
        print(f"  {key}: {value}")

# Flatten nested dictionary
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
```

---

## Sorting Dictionaries

```python
d = {"banana": 3, "apple": 1, "cherry": 2}

# Sort by keys
sorted_by_keys = dict(sorted(d.items()))
# {'apple': 1, 'banana': 3, 'cherry': 2}

# Sort by keys (descending)
sorted_desc = dict(sorted(d.items(), reverse=True))
# {'cherry': 2, 'banana': 3, 'apple': 1}

# Sort by values
sorted_by_values = dict(sorted(d.items(), key=lambda x: x[1]))
# {'apple': 1, 'cherry': 2, 'banana': 3}

# Sort by values (descending)
sorted_by_values_desc = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
# {'banana': 3, 'cherry': 2, 'apple': 1}

# Get keys sorted by values
sorted_keys = sorted(d, key=d.get)
# ['apple', 'cherry', 'banana']

# Get top N items by value
from heapq import nlargest, nsmallest
top_2 = dict(nlargest(2, d.items(), key=lambda x: x[1]))
# {'banana': 3, 'cherry': 2}

bottom_2 = dict(nsmallest(2, d.items(), key=lambda x: x[1]))
# {'apple': 1, 'cherry': 2}
```

---

## Default Values & DefaultDict

```python
# Using get() with default
d = {"a": 1}
value = d.get("b", 0)  # 0 (doesn't add to dict)

# Using setdefault()
d.setdefault("b", 0)   # Adds 'b': 0 to dict and returns 0

# defaultdict - Auto-creates default values
from collections import defaultdict

# Default to 0 (for counting)
counter = defaultdict(int)
counter["a"] += 1
counter["b"] += 1
counter["a"] += 1
# defaultdict(int, {'a': 2, 'b': 1})

# Default to empty list (for grouping)
groups = defaultdict(list)
groups["fruits"].append("apple")
groups["fruits"].append("banana")
groups["vegetables"].append("carrot")
# defaultdict(list, {'fruits': ['apple', 'banana'], 'vegetables': ['carrot']})

# Default to empty set
unique_items = defaultdict(set)
unique_items["a"].add(1)
unique_items["a"].add(1)  # Ignored (duplicate)
# defaultdict(set, {'a': {1}})

# Custom default factory
def default_person():
    return {"name": "Unknown", "age": 0}

people = defaultdict(default_person)
print(people["alice"])  # {'name': 'Unknown', 'age': 0}

# Nested defaultdict
tree = lambda: defaultdict(tree)
d = tree()
d["a"]["b"]["c"] = "value"
# {'a': {'b': {'c': 'value'}}}
```

---

## Counter & OrderedDict

### Counter

```python
from collections import Counter

# Create counter from iterable
c = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

c = Counter(["apple", "banana", "apple", "cherry", "apple"])
# Counter({'apple': 3, 'banana': 1, 'cherry': 1})

# Most common elements
c.most_common(2)         # [('apple', 3), ('banana', 1)]

# Access counts
c["apple"]               # 3
c["grape"]               # 0 (doesn't raise KeyError)

# Update counter
c.update(["banana", "banana"])
# Counter({'apple': 3, 'banana': 3, 'cherry': 1})

# Subtract counts
c.subtract(["apple", "apple"])
# Counter({'banana': 3, 'apple': 1, 'cherry': 1})

# Arithmetic operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
c1 + c2                  # Counter({'a': 4, 'b': 3})
c1 - c2                  # Counter({'a': 2}) (negative removed)
c1 & c2                  # Counter({'a': 1, 'b': 1}) (min)
c1 | c2                  # Counter({'a': 3, 'b': 2}) (max)

# Get elements as iterator
list(c.elements())       # ['a', 'a', 'a', 'b']

# Total count
c.total()                # 4 (Python 3.10+)
sum(c.values())          # 4 (all versions)
```

### OrderedDict

```python
from collections import OrderedDict

# Note: Regular dicts maintain insertion order since Python 3.7
# OrderedDict provides additional methods

od = OrderedDict()
od["a"] = 1
od["b"] = 2
od["c"] = 3

# Move to end
od.move_to_end("a")      # {'b': 2, 'c': 3, 'a': 1}
od.move_to_end("c", last=False)  # Move to beginning

# Pop from specific end
od.popitem(last=True)    # Remove last item
od.popitem(last=False)   # Remove first item

# Equality considers order
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
od1 == od2               # False (different order)

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
d1 == d2                 # True (regular dicts ignore order)
```

---

## Useful Patterns & Tricks

### Counting & Grouping

```python
# Count items
from collections import Counter
items = ["a", "b", "a", "c", "a", "b"]
counts = Counter(items)  # Counter({'a': 3, 'b': 2, 'c': 1})

# Group items by attribute
from collections import defaultdict
people = [
    {"name": "Alice", "city": "Paris"},
    {"name": "Bob", "city": "London"},
    {"name": "Charlie", "city": "Paris"}
]
by_city = defaultdict(list)
for person in people:
    by_city[person["city"]].append(person["name"])
# {'Paris': ['Alice', 'Charlie'], 'London': ['Bob']}
```

### Dictionary as Switch/Case

```python
def operation(op, a, b):
    operations = {
        "add": lambda: a + b,
        "sub": lambda: a - b,
        "mul": lambda: a * b,
        "div": lambda: a / b if b != 0 else None
    }
    return operations.get(op, lambda: None)()

operation("add", 5, 3)  # 8
```

### Inverting a Dictionary

```python
original = {"a": 1, "b": 2, "c": 3}

# Simple inversion (assumes unique values)
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Safe inversion (handles duplicate values)
from collections import defaultdict
original = {"a": 1, "b": 2, "c": 1}
inverted = defaultdict(list)
for k, v in original.items():
    inverted[v].append(k)
# {1: ['a', 'c'], 2: ['b']}
```

### Safe Dictionary Access

```python
# Chained get for nested access
data = {"user": {"profile": {"name": "Alice"}}}
name = data.get("user", {}).get("profile", {}).get("name", "Unknown")

# Using try/except
try:
    name = data["user"]["profile"]["name"]
except KeyError:
    name = "Unknown"
```

### Dictionary Unpacking in Functions

```python
def greet(name, age, city):
    return f"{name} is {age} years old and lives in {city}"

person = {"name": "Alice", "age": 30, "city": "Paris"}
greet(**person)  # "Alice is 30 years old and lives in Paris"
```

### Filtering Dictionary

```python
original = {"a": 1, "b": 2, "c": 3, "d": 4}

# Filter by value
filtered = {k: v for k, v in original.items() if v > 2}
# {'c': 3, 'd': 4}

# Filter by key
allowed_keys = {"a", "c"}
filtered = {k: v for k, v in original.items() if k in allowed_keys}
# {'a': 1, 'c': 3}

# Using filter function
filtered = dict(filter(lambda x: x[1] > 2, original.items()))
```

### Transform Dictionary

```python
prices = {"apple": 1.0, "banana": 0.5, "orange": 0.75}

# Transform values
discounted = {k: round(v * 0.9, 2) for k, v in prices.items()}

# Transform keys
upper_keys = {k.upper(): v for k, v in prices.items()}

# Transform both
transformed = {k.upper(): v * 100 for k, v in prices.items()}
```

---

## Key Differences to Remember

| Method/Operation | Behavior |
|------------------|----------|
| `d[key]` | Access value, raises `KeyError` if missing |
| `d.get(key)` | Access value, returns `None` if missing |
| `d.get(key, default)` | Access value, returns `default` if missing |
| `d.setdefault(key, val)` | Get value or set & return default |
| `d.pop(key)` | Remove & return, raises `KeyError` if missing |
| `d.pop(key, default)` | Remove & return, returns `default` if missing |
| `d.update(other)` | Modify in place |
| `d \| other` | Create new merged dict (Python 3.9+) |
| `d.copy()` | Shallow copy |
| `copy.deepcopy(d)` | Deep copy |

---

## Quick Reference Cheat Sheet

```python
# Create
d = {"a": 1, "b": 2}
d = dict(a=1, b=2)
d = dict.fromkeys(["a", "b"], 0)

# Access
d["a"]           d.get("a")          d.get("a", default)
d.keys()         d.values()          d.items()

# Add/Update
d["c"] = 3       d.update({"d": 4})  d.setdefault("e", 5)

# Remove
d.pop("a")       d.popitem()         del d["b"]          d.clear()

# Check
"a" in d         len(d)              "x" in d.values()

# Iterate
for k in d:                    # keys
for v in d.values():           # values
for k, v in d.items():         # both

# Merge (Python 3.9+)
merged = d1 | d2               # new dict
d1 |= d2                       # in-place

# Comprehension
{k: v*2 for k, v in d.items()}
{k: v for k, v in d.items() if v > 1}

# Special
from collections import defaultdict, Counter, OrderedDict
```

---

## License

This guide is free to use and share.