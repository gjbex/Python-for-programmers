'''
Implementation of an intersection tree approach for efficiently finding
intersections among a set of query intervals and a database intervals.

This module provides:
- Node: A tree node representing an interval with efficient intersection search
- Utility functions for generating intervals, creating databases, and executing queries

Note: The tree structure is a binary search tree ordered by interval start points.
In worst case scenarios (e.g., with sorted input), the tree may become unbalanced
and degrade to O(n) performance instead of the optimal O(log n).

Example usage:
    >>> from intersection_tree import create_db, create_queries, execute_queries
    >>> db = create_db(size=100)
    >>> queries = create_queries(size=10)
    >>> results = execute_queries(queries, db)
'''

import random
import typing


Interval: typing.TypeAlias = tuple[int, int]
Queries: typing.TypeAlias = list[Interval]
QueryResult: typing.TypeAlias = list[tuple[Interval, Interval]]

class Node:
    '''Class representing a node in an intersection tree.
    
    Each node represents an interval in the dataset, so it has the start and the
    end of that interval.  It also contains a reference to its left and right child.
    For indexing purposes, it also contains the maximum end value over all its children.
    '''

    def __init__(self, interval: Interval) -> None:
        '''Initialize node representing the interval [start, end).

        Parameters
        ----------
        interval: Interval
            the interval represented by this node
        '''
        if interval[0] >= interval[1]:
            raise ValueError(f"Invalid interval: start ({interval[0]}) must be less than end ({interval[1]})")
        
        self._start: int = interval[0]
        self._end: int = interval[1]
        self._max_end: int = interval[1]
        self._left: 'Node | None' = None
        self._right: 'Node | None' = None

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
            
        if interval[0] < self._start:
            if self._left is None:
                self._left = Node(interval)
            else:
                self._left.insert(interval)
        else:
            if self._right is None:
                self._right = Node(interval)
            else:
                self._right.insert(interval)
        self._max_end = max(self._max_end, interval[1])

    def search(self, interval: Interval, results: list[Interval]) -> None:
        '''Search for all intervals in the tree that intersect with [start, end)
        and append them to results.

        Parameters
        ----------
        interval: Interval
            the interval to search for intersections
        results: list[Interval]
            list to append the results to
        '''
        if self._start < interval[1] and interval[0] < self._end:
            results.append((self._start, self._end))
        if self._left is not None and self._left._max_end >= interval[0]:
            self._left.search(interval, results)
        if self._right is not None and self._right._max_end >= interval[0]:
            self._right.search(interval, results)

    def to_str(self, prefix: str = '') -> str:
        '''Return a string representation of the tree.

        Parameters
        ----------
        prefix: str
            prefix to add to each line, default is empty string

        Returns
        -------
        str
            string representation of the tree
        '''
        result = f'{prefix}[{self._start}, {self._end}] (max_end={self._max_end})\n'
        if self._left is not None:
            result += self._left.to_str(prefix + '  ')
        if self._right is not None:
            result += self._right.to_str(prefix + '  ')
        return result

    def __repr__(self) -> str:
        '''Return a string representation of the node.

        Returns
        -------
        str
            string representation of the node
        '''
        return f'Node({self._start}, {self._end}, max_end={self._max_end})'

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


def create_db(size: int, max_end: int = 1_000_000) -> Node:
    '''Generate a database of intervals and return the intersection tree.

    Parameters
    ----------
    size: int
        number of intervals in the database
    max_end: int
        largest end value of the interval, default value 1_000_000

    Returns
    -------
    Node
        root of the intersection tree
    '''
    tree = Node(generate_interval(max_end))
    for _ in range(1, size):
        tree.insert(generate_interval(max_end))
    return tree


def execute_queries(queries: Queries, db: Node) -> QueryResult:
    '''Execute the query on the database

    Parameters
    ----------
    queries: Queries
        queries to be executed
    db: Node
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


def populate_db(db: Node | None, intervals: typing.Sequence[Interval]) -> Node:
    if len(intervals) == 0:
        raise ValueError('At least 1 interval is required')
    if db is None:
        db = Node(intervals[0])
        # Start from index 1 since we used the first interval for the root
        start_index = 1
    else:
        start_index = 0
    for i in range(start_index, len(intervals)):
        db.insert(intervals[i])
    return db