import random
import time
from functools import lru_cache


def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


def update_no_cache(array, index, value):
    array[index] = value


# Using LRU cache
@lru_cache(maxsize=1000)
def range_sum_with_cache(array_id, L, R):
    return sum(array[L : R + 1])


def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()


if __name__ == "__main__":
    # Random array
    N = 100_000
    array = [random.randint(1, 100) for _ in range(N)]

    # Generate 50,000 random queries
    Q = 50_000
    queries = []
    for _ in range(Q):
        if random.random() < 0.5:
            # Range query
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            # Update query
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(("Update", index, value))

    # Measure execution time without cache
    print("Executing queries without cache...")
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            _, L, R = query
            range_sum_no_cache(array, L, R)
        elif query[0] == "Update":
            _, index, value = query
            update_no_cache(array, index, value)
    no_cache_time = time.time() - start_time
    print(f"Execution time without cache: {no_cache_time:.2f} seconds")

    # Measure execution time with LRU cache
    print("Executing queries with LRU cache...")
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            _, L, R = query
            range_sum_with_cache(id(array), L, R)
        elif query[0] == "Update":
            _, index, value = query
            update_with_cache(array, index, value)
    cache_time = time.time() - start_time
    print(f"Execution time with LRU cache: {cache_time:.2f} seconds")
