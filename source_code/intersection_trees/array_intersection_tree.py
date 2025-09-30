'''
Array-based implementation of an intersection tree for efficiently finding
intersections among a set of query intervals and a database intervals.

This module provides an alternative implementation using arrays instead of
traditional tree node objects, potentially offering better cache locality
and performance for large datasets.

The Tree object contains arrays start, end, max_end, left, and right.
A node is represented by an index into these arrays, and left/right
refer to the indices of respective child nodes (-1 indicates None).

Example usage:
    >>> from array_intersection_tree import ArrayTree, create_db, create_queries, execute_queries
    >>> db = create_db(size=100)
    >>> queries = create_queries(size=10)
    >>> results = execute_queries(queries, db)
'''

import random
import typing


Interval: typing.TypeAlias = tuple[int, int]
Queries: typing.TypeAlias = list[Interval]
QueryResult: typing.TypeAlias = list[tuple[Interval, Interval]]


class ArrayTree:
    '''Array-based intersection tree implementation.

    Each node is represented by an index, and the tree data is stored in
    arrays:
    - start[i]: start value of interval at node i
    - end[i]: end value of interval at node i
    - max_end[i]: maximum end value in subtree rooted at node i
    - left[i]: index of left child of node i (-1 if None)
    - right[i]: index of right child of node i (-1 if None)
    '''

    def __init__(self, initial_capacity: int = 1000) -> None:
        '''Initialize empty array-based tree with given initial capacity.

        Parameters
        ----------
        initial_capacity: int
            initial capacity of the arrays, default 1000
        '''
        self._capacity = initial_capacity
        self._size = 0
        self._root = -1  # -1 indicates empty tree

        # Initialize arrays
        self.start = [-1] * self._capacity
        self.end = [-1] * self._capacity
        self.max_end = [-1] * self._capacity
        self.left = [-1] * self._capacity
        self.right = [-1] * self._capacity

    def _resize(self) -> None:
        '''Double the capacity of all arrays when needed.'''
        old_capacity = self._capacity
        self._capacity *= 2

        # Resize all arrays
        self.start.extend([-1] * old_capacity)
        self.end.extend([-1] * old_capacity)
        self.max_end.extend([-1] * old_capacity)
        self.left.extend([-1] * old_capacity)
        self.right.extend([-1] * old_capacity)

    def insert(self, interval: Interval) -> None:
        '''Insert a new interval [start, end) in the tree.

        Parameters
        ----------
        interval: Interval
            the interval to insert

        Raises
        ------
        ValueError
            if interval start is not less than end
        '''
        if interval[0] >= interval[1]:
            raise ValueError(f"Invalid interval: start ({interval[0]}) must be less than end ({interval[1]})")

        if self._root == -1:
            # Tree is empty, create root
            if self._size >= self._capacity:
                self._resize()
            self._root = 0
            self.start[0] = interval[0]
            self.end[0] = interval[1]
            self.max_end[0] = interval[1]
            self.left[0] = -1
            self.right[0] = -1
            self._size = 1
        else:
            self._insert_at(self._root, interval)

    def _insert_at(self, node_idx: int, interval: Interval) -> None:
        '''Insert interval at the subtree rooted at node_idx.

        Parameters
        ----------
        node_idx: int
            index of the root of the subtree
        interval: Interval
            the interval to insert
        '''
        # Update max_end for current node
        self.max_end[node_idx] = max(self.max_end[node_idx], interval[1])

        if interval[0] < self.start[node_idx]:
            # Insert in left subtree
            if self.left[node_idx] == -1:
                # Create new left child
                if self._size >= self._capacity:
                    self._resize()
                new_idx = self._size
                self.start[new_idx] = interval[0]
                self.end[new_idx] = interval[1]
                self.max_end[new_idx] = interval[1]
                self.left[new_idx] = -1
                self.right[new_idx] = -1
                self.left[node_idx] = new_idx
                self._size += 1
            else:
                self._insert_at(self.left[node_idx], interval)
        else:
            # Insert in right subtree
            if self.right[node_idx] == -1:
                # Create new right child
                if self._size >= self._capacity:
                    self._resize()
                new_idx = self._size
                self.start[new_idx] = interval[0]
                self.end[new_idx] = interval[1]
                self.max_end[new_idx] = interval[1]
                self.left[new_idx] = -1
                self.right[new_idx] = -1
                self.right[node_idx] = new_idx
                self._size += 1
            else:
                self._insert_at(self.right[node_idx], interval)

    def search(self, interval: Interval, results: list[Interval]) -> None:
        '''Search for all intervals in the tree that intersect with
        [start, end) and append them to results.

        Parameters
        ----------
        interval: Interval
            the interval to search for intersections
        results: list[Interval]
            list to append the results to

        Raises
        ------
        ValueError
            if interval start is not less than end
        '''
        if interval[0] >= interval[1]:
            raise ValueError(f"Invalid interval: start ({interval[0]}) must be less than end ({interval[1]})")

        if self._root != -1:
            self._search_at(self._root, interval, results)

    def _search_at(self, node_idx: int, interval: Interval, results: list[Interval]) -> None:
        '''Search for intersections in subtree rooted at node_idx.

        Parameters
        ----------
        node_idx: int
            index of the root of the subtree
        interval: Interval
            the interval to search for intersections
        results: list[Interval]
            list to append the results to
        '''
        # Check if current node's interval intersects with query interval
        if self.start[node_idx] < interval[1] and interval[0] < self.end[node_idx]:
            results.append((self.start[node_idx], self.end[node_idx]))

        # Search left subtree if it might contain intersections
        left_idx = self.left[node_idx]
        if left_idx != -1 and self.max_end[left_idx] >= interval[0]:
            self._search_at(left_idx, interval, results)

        # Search right subtree if it might contain intersections
        right_idx = self.right[node_idx]
        if right_idx != -1 and self.max_end[right_idx] >= interval[0]:
            self._search_at(right_idx, interval, results)

    def size(self) -> int:
        '''Return the number of intervals in the tree.

        Returns
        -------
        int
            number of intervals stored in the tree
        '''
        return self._size

    def is_empty(self) -> bool:
        '''Check if the tree is empty.

        Returns
        -------
        bool
            True if the tree is empty, False otherwise
        '''
        return self._root == -1

    def to_str(self, node_idx: int | None = None, prefix: str = '') -> str:
        '''Return a string representation of the tree.

        Parameters
        ----------
        node_idx: int, optional
            index of the node to start from, default is root
        prefix: str
            prefix to add to each line, default is empty string

        Returns
        -------
        str
            string representation of the tree
        '''
        if node_idx is None:
            if self._root == -1:
                return f'{prefix}Empty tree\n'
            node_idx = self._root

        result = f'{prefix}[{self.start[node_idx]}, {self.end[node_idx]}] (max_end={self.max_end[node_idx]}) @{node_idx}\n'

        left_idx = self.left[node_idx]
        if left_idx != -1:
            result += self.to_str(left_idx, prefix + '  ')
            
        right_idx = self.right[node_idx]
        if right_idx != -1:
            result += self.to_str(right_idx, prefix + '  ')

        return result

    def __str__(self) -> str:
        '''Return a string representation of the tree.

        Returns
        -------
        str
            string representation of the tree
        '''
        return self.to_str()


def generate_interval(max_end: int = 1_000_000_000) -> Interval:
    '''Generate a half-open interval of at least length 1

    Parameters
    ----------
    max_end: int
        largest end value of the interval, default value 1_000_000_000

    Returns
    -------
    Interval
        Tuple (start, end) such that end - start > 1

    Raises
    ------
    ValueError
        if max_end is less than 2
    '''
    if max_end < 2:
        raise ValueError(f"max_end must be at least 2, got {max_end}")

    start = random.randint(0, max_end - 2)
    end = random.randint(start + 2, max_end)
    return start, end


def create_db(size: int, max_end: int = 1_000_000) -> ArrayTree:
    '''Generate a database of intervals and return the array-based
    intersection tree.

    Parameters
    ----------
    size: int
        number of intervals in the database
    max_end: int
        largest end value of the interval, default value 1_000_000

    Returns
    -------
    ArrayTree
        array-based intersection tree containing the intervals
    '''
    tree = ArrayTree(initial_capacity=max(size, 1000))
    for _ in range(size):
        tree.insert(generate_interval(max_end))
    return tree


def execute_queries(queries: Queries, db: ArrayTree) -> QueryResult:
    '''Execute the query on the database

    Parameters
    ----------
    queries: Queries
        queries to be executed
    db: ArrayTree
        database to query

    Returns
    -------
    QueryResult
        set of tuples of query and database intervals that intersect
    '''
    results: QueryResult = []
    for q in queries:
        db_results: list[Interval] = []
        db.search(q, db_results)
        results.extend((q, d) for d in db_results)
    return results


def create_queries(size: int = 1_000, max_end: int = 1_000_000) -> Queries:
    '''Generate query intervals.
    
    Parameters
    ----------
    size: int
        number of intervals in the query, default value 1_000
    max_end: int
        largest end value of the interval, default value 1_000_000

    Returns
    -------
    Queries
        a list of half-open intervals
    '''
    return [generate_interval(max_end) for _ in range(size)]


def populate_db(db: ArrayTree | None, intervals: typing.Sequence[Interval]) -> ArrayTree:
    '''Populate an existing database with additional intervals or
    create a new one.

    Parameters
    ----------
    db: ArrayTree | None
        existing database to populate, if None a new database is created
    intervals: typing.Sequence[Interval]
        intervals to insert into the database

    Returns
    -------
    ArrayTree
        the populated array-based intersection tree

    Raises
    ------
    ValueError
        if intervals is empty
    '''
    if len(intervals) == 0:
        raise ValueError('At least 1 interval is required')

    if db is None:
        db = ArrayTree(initial_capacity=max(len(intervals), 1000))

    for interval in intervals:
        db.insert(interval)
    return db


def plot_intersection_tree(tree: ArrayTree) -> None:
    """Visualize the array-based intersection tree using :mod:`matplotlib`.

    Each node in the tree is drawn as a horizontal line spanning the interval
    ``[start, end]``.  The root of the tree is shown at the bottom of the
    figure, with each subsequent level plotted above it.  The start and end
    values of the interval are annotated next to their respective end points
    together with the ``max_end`` value for that node.  Lines are also drawn
    from the midpoint of each interval to the midpoints of its children to
    illustrate the tree structure.

    Parameters
    ----------
    tree: ArrayTree
        Array-based intersection tree to plot.
    """

    import matplotlib.pyplot as plt

    if tree.is_empty():
        return

    # Collect all nodes along with their depth in the tree.
    nodes: list[tuple[int, int]] = []  # (node_idx, depth)

    def _traverse(node_idx: int, depth: int) -> None:
        if node_idx == -1:
            return
        nodes.append((node_idx, depth))
        _traverse(tree.left[node_idx], depth + 1)
        _traverse(tree.right[node_idx], depth + 1)

    _traverse(tree._root, 0)

    if not nodes:
        return

    _, ax = plt.subplots()
    max_depth = max(depth for _, depth in nodes)

    # Draw intervals and record midpoints for connecting lines.
    midpoints: dict[int, tuple[float, int]] = {}
    for node_idx, depth in nodes:
        start, end, max_end = tree.start[node_idx], tree.end[node_idx], tree.max_end[node_idx]
        y = depth
        ax.hlines(y, start, end, colors="tab:blue")
        ax.plot([start, end], [y, y], "o", color="tab:blue", markersize=3)
        ax.text(start, y + 0.1, f"{start}", ha="center", va="bottom", fontsize=8)
        ax.text(end, y + 0.1, f"{end}", ha="center", va="bottom", fontsize=8)
        ax.text(end, y - 0.1, f"max={max_end}@{node_idx}", ha="left", va="top", fontsize=8)
        midpoints[node_idx] = ((start + end) / 2, y)

    # Connect each node's midpoint to its children's midpoints.
    for node_idx, depth in nodes:
        parent_mid, parent_y = midpoints[node_idx]
        left_idx = tree.left[node_idx]
        if left_idx != -1:
            child_mid, child_y = midpoints[left_idx]
            ax.plot([parent_mid, child_mid], [parent_y, child_y], color="tab:gray")
        right_idx = tree.right[node_idx]
        if right_idx != -1:
            child_mid, child_y = midpoints[right_idx]
            ax.plot([parent_mid, child_mid], [parent_y, child_y], color="tab:gray")

    ax.set_xlabel("value")
    ax.set_ylabel("depth")
    ax.set_ylim(-1, max_depth + 1)
    ax.set_title("Array-based Intersection tree")
    plt.show()
