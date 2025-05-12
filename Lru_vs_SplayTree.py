import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Insert a key-value pair into the Splay Tree."""
        if self.root is None:
            self.root = Node((key, value))
        else:
            self._insert_node((key, value), self.root)

    def _insert_node(self, data, current_node):
        """Recursive insertion of a key-value pair."""
        key, _ = data
        if key < current_node.data[0]:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def search(self, key):
        """Search for a key in the Splay Tree and return its value."""
        node = self.root
        while node is not None:
            if key < node.data[0]:
                node = node.left_node
            elif key > node.data[0]:
                node = node.right_node
            else:
                self._splay(node)
                return node.data[1]
        return None  # Key not found

    def _splay(self, node):
        """Splay operation to move the node to the root."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig case
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):  # Zig-Zig case
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):  # Zig-Zig case
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag case
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Right rotation of a node."""
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Left rotation of a node."""
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


# Fibonacci using Splay Tree
def fibonacci_splay(n, tree):
    result = tree.search(n)
    if result is not None:
        return result
    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


if __name__ == "__main__":
    # Fibonacci numbers to calculate
    fibonacci_numbers = list(range(0, 951, 50))

    # Measure performance for LRU Cache
    lru_times = []
    for n in fibonacci_numbers:
        time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(time)

    # Measure performance for Splay Tree
    splay_times = []
    for n in fibonacci_numbers:
        tree = SplayTree()
        time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(time)

    # Print table
    print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
    print("-" * 50)
    for n, lru_time, splay_time in zip(fibonacci_numbers, lru_times, splay_times):
        print(f"{n:<10}{lru_time:<20.8f}{splay_time:<20.8f}")

    # Visualize the results
    plt.figure(figsize=(10, 6))
    plt.plot(fibonacci_numbers, lru_times, label="LRU Cache", marker="o")
    plt.plot(fibonacci_numbers, splay_times, label="Splay Tree", marker="x")
    plt.xlabel("Fibonacci Number (n)")
    plt.ylabel("Average Execution Time (seconds)")
    plt.title("Comparison of Execution Time for LRU Cache and Splay Tree")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
