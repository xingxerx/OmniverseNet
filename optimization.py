# optimization_examples.py

import time
import functools
import random
from memory_profiler import profile # You might need to install: pip install memory_profiler psutil

# --- 1. Profiling Target ---
# A function that does some work, suitable for profiling
def process_data(data_list):
    """Simulates processing a list of data."""
    processed = []
    for item in data_list:
        # Simulate some computation
        time.sleep(0.001)
        processed.append(item * item)
    return processed

# --- 2. Efficient Data Structures ---
def check_membership_list(data, items_to_check):
    """Checks membership using a list (less efficient for large lists)."""
    count = 0
    for item in items_to_check:
        if item in data: # O(n) lookup for lists
            count += 1
    return count

def check_membership_set(data_set, items_to_check):
    """Checks membership using a set (more efficient)."""
    count = 0
    for item in items_to_check:
        if item in data_set: # O(1) average lookup for sets
            count += 1
    return count

# --- 3. List Comprehensions vs. Loops ---
def create_list_with_loop(n):
    """Creates a list of squares using a for loop."""
    squares = []
    for i in range(n):
        squares.append(i * i)
    return squares

def create_list_with_comprehension(n):
    """Creates a list of squares using list comprehension."""
    return [i * i for i in range(n)]

# --- 4. Efficient String Concatenation ---
def join_strings_with_plus(string_list):
    """Joins strings using the '+' operator (less efficient)."""
    result = ""
    for s in string_list:
        result += s + ","
    return result

def join_strings_with_join(string_list):
    """Joins strings using the 'join' method (more efficient)."""
    return ",".join(string_list)

# --- 5. Caching with LRU Cache ---
@functools.lru_cache(maxsize=128)
def expensive_calculation(a, b):
    """Simulates an expensive calculation that benefits from caching."""
    print(f"Performing expensive calculation for ({a}, {b})...")
    time.sleep(0.5) # Simulate computational cost
    return (a * a) + (b * b)

# --- Demonstration ---
if __name__ == "__main__":
    print("--- Optimization Examples ---")

    # Data for examples
    large_number = 10000
    data_list = list(range(large_number))
    data_set = set(data_list)
    items_to_check = [random.randint(0, large_number * 2) for _ in range(large_number // 2)]
    string_list = [str(i) for i in range(1000)]

    # Example 1: Profiling (Run this script with python -m cProfile optimization_examples.py)
    print("\n1. Profiling Target (run with cProfile):")
    # process_data(data_list[:100]) # Keep it short for inline demo
    print("   (Run 'python -m cProfile optimization_examples.py' to see profiling)")


    # Example 2: Data Structures
    print("\n2. Data Structure Efficiency (Membership Checking):")
    start_time = time.time()
    count1 = check_membership_list(data_list, items_to_check)
    print(f"   List check time: {time.time() - start_time:.4f}s (Found: {count1})")

    start_time = time.time()
    count2 = check_membership_set(data_set, items_to_check)
    print(f"   Set check time:  {time.time() - start_time:.4f}s (Found: {count2})")

    # Example 3: List Comprehensions
    print("\n3. List Creation Efficiency:")
    start_time = time.time()
    list1 = create_list_with_loop(large_number)
    print(f"   Loop time:        {time.time() - start_time:.4f}s")

    start_time = time.time()
    list2 = create_list_with_comprehension(large_number)
    print(f"   Comprehension time: {time.time() - start_time:.4f}s")

    # Example 4: String Concatenation
    print("\n4. String Joining Efficiency:")
    start_time = time.time()
    str1 = join_strings_with_plus(string_list)
    print(f"   Plus (+) time: {time.time() - start_time:.4f}s (Length: {len(str1)})")

    start_time = time.time()
    str2 = join_strings_with_join(string_list)
    print(f"   Join() time:   {time.time() - start_time:.4f}s (Length: {len(str2)})")

    # Example 5: Caching
    print("\n5. Caching with lru_cache:")
    print("   First call (5, 6):")
    res1 = expensive_calculation(5, 6)
    print(f"   Result: {res1}")

    print("   Second call (5, 6) - should be faster:")
    res2 = expensive_calculation(5, 6)
    print(f"   Result: {res2}")

    print("   First call (7, 8):")
    res3 = expensive_calculation(7, 8)
    print(f"   Result: {res3}")

    print("   Second call (7, 8) - should be faster:")
    res4 = expensive_calculation(7, 8)
    print(f"   Result: {res4}")

    print("\n--- End Examples ---")

    # Optional: Memory Profiling Example
    # To use this, uncomment the @profile decorator above process_data
    # and run with: python -m memory_profiler optimization_examples.py
    # print("\nRunning memory profile target...")
    # processed_data = process_data(data_list[:500])
    # print(f"Memory profiled function finished. Output length: {len(processed_data)}")

