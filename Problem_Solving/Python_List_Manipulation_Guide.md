# Python List (Array) Manipulation Guide

A comprehensive reference for working with lists in Python.

---

## Table of Contents

1. [Creating Lists](#creating-lists)
2. [Accessing Elements](#accessing-elements)
3. [Adding Elements](#adding-elements)
4. [Removing Elements](#removing-elements)
5. [Modifying Elements](#modifying-elements)
6. [Searching & Counting](#searching--counting)
7. [Sorting & Reversing](#sorting--reversing)
8. [Copying Lists](#copying-lists)
9. [Useful Built-in Functions](#useful-built-in-functions)
10. [List Comprehensions](#list-comprehensions)
11. [Unpacking](#unpacking)
12. [Zipping & Enumerating](#zipping--enumerating)
13. [NumPy Arrays](#numpy-arrays-for-numerical-work)
14. [Key Differences to Remember](#key-differences-to-remember)

---

## Creating Lists

```python
# Empty list
my_list = []
my_list = list()

# With elements
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# From range
numbers = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# List comprehension
squares = [x**2 for x in range(10)]

# Repeat elements
zeros = [0] * 5  # [0, 0, 0, 0, 0]
```

---

## Accessing Elements

```python
lst = [10, 20, 30, 40, 50]

# Single element access
lst[0]       # First element → 10
lst[1]       # Second element → 20
lst[-1]      # Last element → 50
lst[-2]      # Second to last → 40

# Slicing [start:stop:step]
lst[1:3]     # From index 1 to 2 → [20, 30]
lst[:3]      # First 3 elements → [10, 20, 30]
lst[2:]      # From index 2 to end → [30, 40, 50]
lst[::2]     # Every 2nd element → [10, 30, 50]
lst[1::2]    # Every 2nd starting at index 1 → [20, 40]
lst[::-1]    # Reversed list → [50, 40, 30, 20, 10]
lst[-3:-1]   # Negative slice → [30, 40]
```

---

## Adding Elements

```python
lst = [10, 20, 30]

# append() - Add single element to end
lst.append(40)           # [10, 20, 30, 40]

# insert() - Add element at specific index
lst.insert(0, 5)         # [5, 10, 20, 30, 40]
lst.insert(2, 15)        # [5, 10, 15, 20, 30, 40]

# extend() - Add multiple elements
lst.extend([50, 60])     # [5, 10, 15, 20, 30, 40, 50, 60]

# Concatenation with +
new_lst = lst + [70, 80]

# In-place concatenation with +=
lst += [70, 80]
```

---

## Removing Elements

```python
lst = [10, 20, 30, 40, 50, 30]

# pop() - Remove and return element by index
last = lst.pop()         # Returns 30, lst = [10, 20, 30, 40, 50]
first = lst.pop(0)       # Returns 10, lst = [20, 30, 40, 50]

# remove() - Remove first occurrence of value
lst.remove(30)           # lst = [20, 40, 50]

# del - Delete by index or slice
del lst[0]               # Delete first element
del lst[1:3]             # Delete slice
del lst[:]               # Delete all elements

# clear() - Remove all elements
lst.clear()              # lst = []
```

---

## Modifying Elements

```python
lst = [10, 20, 30, 40, 50]

# Replace single element
lst[0] = 100             # [100, 20, 30, 40, 50]

# Replace slice
lst[1:3] = [200, 300]    # [100, 200, 300, 40, 50]

# Replace with different length
lst[1:3] = [1, 2, 3, 4]  # Expands the list

# Insert via slice
lst[2:2] = [25]          # Inserts 25 at index 2
```

---

## Searching & Counting

```python
lst = [10, 20, 30, 20, 40]

# Check if element exists
20 in lst                # True
100 in lst               # False
100 not in lst           # True

# Find index of element
lst.index(30)            # 2
lst.index(20)            # 0 (first occurrence)
lst.index(20, 2)         # 3 (search starting from index 2)

# Count occurrences
lst.count(20)            # 2
lst.count(100)           # 0

# Safe index search (avoid ValueError)
def safe_index(lst, value):
    return lst.index(value) if value in lst else -1
```

---

## Sorting & Reversing

```python
lst = [3, 1, 4, 1, 5, 9, 2, 6]

# sort() - Sort in place
lst.sort()                      # [1, 1, 2, 3, 4, 5, 6, 9]
lst.sort(reverse=True)          # [9, 6, 5, 4, 3, 2, 1, 1]

# Sort with custom key
words = ["banana", "pie", "apple"]
words.sort(key=len)             # ['pie', 'apple', 'banana']
words.sort(key=str.lower)       # Case-insensitive sort

# sorted() - Return new sorted list (original unchanged)
original = [3, 1, 4]
new_sorted = sorted(original)   # original still [3, 1, 4]

# reverse() - Reverse in place
lst.reverse()

# reversed() - Return iterator
for item in reversed(lst):
    print(item)

# Create reversed list
reversed_lst = list(reversed(lst))
reversed_lst = lst[::-1]        # Alternative using slice
```

---

## Copying Lists

```python
original = [[1, 2], [3, 4]]

# Shallow copy methods (copy references for nested objects)
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

# Deep copy (completely independent copy)
import copy
deep = copy.deepcopy(original)

# Demonstration of shallow vs deep copy
original[0][0] = 999
print(copy1[0][0])    # 999 (affected by change)
print(deep[0][0])     # 1 (not affected)
```

---

## Useful Built-in Functions

```python
lst = [10, 20, 30, 40, 50]

# Length
len(lst)                 # 5

# Min and Max
min(lst)                 # 10
max(lst)                 # 50

# Sum
sum(lst)                 # 150
sum(lst, start=10)       # 160 (with initial value)

# Any and All
any([False, True, False])    # True (at least one truthy)
all([True, True, True])      # True (all truthy)
all([True, False, True])     # False

# Map (apply function to all elements)
list(map(str, [1, 2, 3]))           # ['1', '2', '3']
list(map(lambda x: x*2, [1, 2, 3])) # [2, 4, 6]

# Filter
list(filter(lambda x: x > 2, [1, 2, 3, 4]))  # [3, 4]

# Reduce
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])     # 10
```

---

## List Comprehensions

```python
# Basic syntax: [expression for item in iterable]
[x * 2 for x in range(5)]                    # [0, 2, 4, 6, 8]

# With condition (filter)
[x for x in range(10) if x % 2 == 0]         # [0, 2, 4, 6, 8]

# With if-else (ternary)
[x if x > 0 else 0 for x in [-1, 2, -3, 4]]  # [0, 2, 0, 4]

# Multiple conditions
[x for x in range(20) if x % 2 == 0 if x % 3 == 0]  # [0, 6, 12, 18]

# Nested loops
[(x, y) for x in range(3) for y in range(3)]
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Nested list comprehension (2D list)
[[j for j in range(3)] for i in range(2)]    # [[0,1,2], [0,1,2]]

# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6]]
[item for sublist in nested for item in sublist]  # [1, 2, 3, 4, 5, 6]

# With function calls
[str(x).upper() for x in ['a', 'b', 'c']]    # ['A', 'B', 'C']
```

---

## Unpacking

```python
# Basic unpacking
a, b, c = [1, 2, 3]              # a=1, b=2, c=3

# Extended unpacking with *
first, *rest = [1, 2, 3, 4]      # first=1, rest=[2, 3, 4]
*start, last = [1, 2, 3, 4]      # start=[1, 2, 3], last=4
first, *mid, last = [1, 2, 3, 4] # first=1, mid=[2, 3], last=4

# Swap values
a, b = b, a

# Ignore values with _
first, _, third = [1, 2, 3]      # Ignore second element
first, *_, last = [1, 2, 3, 4]   # Ignore middle elements

# Unpack in function calls
def func(a, b, c):
    return a + b + c

args = [1, 2, 3]
func(*args)                       # Equivalent to func(1, 2, 3)
```

---

## Zipping & Enumerating

```python
# enumerate() - Get index and value
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start from different index
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")

# zip() - Combine multiple iterables
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['Paris', 'London', 'Berlin']

# Basic zip
list(zip(names, ages))  
# [('Alice', 25), ('Bob', 30), ('Charlie', 35)]

# Multiple iterables
list(zip(names, ages, cities))
# [('Alice', 25, 'Paris'), ('Bob', 30, 'London'), ('Charlie', 35, 'Berlin')]

# Unzip with zip(*...)
pairs = [('a', 1), ('b', 2), ('c', 3)]
letters, numbers = zip(*pairs)
# letters = ('a', 'b', 'c'), numbers = (1, 2, 3)

# Create dictionary from two lists
dict(zip(names, ages))  
# {'Alice': 25, 'Bob': 30, 'Charlie': 35}

# zip_longest (for unequal lengths)
from itertools import zip_longest
list(zip_longest([1, 2], [1, 2, 3], fillvalue=0))
# [(1, 1), (2, 2), (0, 3)]
```

---

## NumPy Arrays (for numerical work)

For high-performance numerical operations, use NumPy arrays:

```python
import numpy as np

# Creating arrays
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros(5)              # [0., 0., 0., 0., 0.]
ones = np.ones(5)                # [1., 1., 1., 1., 1.]
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)  # [0., 0.25, 0.5, 0.75, 1.]

# Element-wise operations
arr * 2                          # [2, 4, 6, 8, 10]
arr + arr                        # [2, 4, 6, 8, 10]
arr ** 2                         # [1, 4, 9, 16, 25]

# Reshaping
arr = np.array([1, 2, 3, 4, 5, 6])
arr.reshape(2, 3)                # 2x3 matrix
arr.reshape(3, 2)                # 3x2 matrix

# Useful methods
arr.sum()                        # Sum of all elements
arr.mean()                       # Average
arr.std()                        # Standard deviation
arr.max()                        # Maximum
arr.argmax()                     # Index of maximum

# Boolean indexing
arr = np.array([1, 2, 3, 4, 5])
arr[arr > 3]                     # [4, 5]
```

---

## Key Differences to Remember

| Method | Behavior |
|--------|----------|
| `append(x)` | Adds **one** element to end |
| `extend([x, y])` | Adds **multiple** elements to end |
| `sort()` | Modifies list **in place**, returns `None` |
| `sorted(lst)` | Returns **new** sorted list |
| `remove(x)` | Deletes by **value** (first occurrence) |
| `pop(i)` / `del lst[i]` | Deletes by **index** |
| `lst[:]` | Creates **shallow** copy |
| `copy.deepcopy(lst)` | Creates **deep** copy |
| `reverse()` | Modifies **in place** |
| `reversed(lst)` | Returns **iterator** |

---

## Quick Reference Cheat Sheet

```python
# Create
lst = [1, 2, 3]

# Access
lst[0]    lst[-1]    lst[1:3]    lst[::-1]

# Add
lst.append(4)    lst.insert(0, 0)    lst.extend([5, 6])

# Remove
lst.pop()    lst.remove(3)    del lst[0]    lst.clear()

# Search
3 in lst    lst.index(3)    lst.count(3)

# Sort
lst.sort()    sorted(lst)    lst.reverse()

# Info
len(lst)    min(lst)    max(lst)    sum(lst)

# Transform
[x*2 for x in lst]    list(map(func, lst))    list(filter(func, lst))
```

---

## License

This guide is free to use and share.