'''
Naive but not Pythonic implementation of interval intersection queries.
'''

import collections
import itertools
import random
import typing


Interval: typing.TypeAlias = tuple[int, int]
Db: typing.TypeAlias = list[Interval]
Queries: typing.TypeAlias = Db
QueryResult: typing.TypeAlias = list[tuple[Interval, Interval]]

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
    '''
    start = random.randint(0, max_end - 2)
    end = random.randint(start + 2, max_end)
    return start, end


def create_db(size: int = 1_000, max_end: int = 1_000_000) -> Db:
    '''Generate a database of intervals
    
    Parameters
    ----------
    size: int
        number of intervals in the database, default value 1_000
    max_end: int
        largest end value of the interval, default value 1_000_000_000

    Returns
    -------
    Db
        a list of half-open intervals
    '''
    return [generate_interval(max_end) for _ in range(size)]


def create_queries(size: int = 1_000, max_end: int = 1_000_000) -> Queries:
    '''Generate query intervals
    
    Parameters
    ----------
    size: int
        number of intervals in the query, default value 1_000
    max_end: int
        largest end value of the interval, default value 1_000_000_000

    Returns
    -------
    Queries
        a list of half-open intervals
    '''
    return create_db(size=size, max_end=max_end)


def have_intersection(q: Interval, d: Interval) -> bool:
    '''Check whether two intervals intersect
    
    Parameters
    ----------
    q, d: Interval
        intervals to check intersection for
        
    Returns
    -------
    bool
        True if q and d intersect, False otherwise
    '''
    return q[0] < d[1] and d[0] < q[1]


def execute_queries(queries: Queries, db: Db) -> QueryResult:
    '''Execute the query on the database

    Parameters
    ----------
    queries: Queries
        queries to be executed
    db: Db
        database to query

    Returns
    -------
    QueryResult
        set of tuples of query and database intervals that intersect
    '''
    return {(q, d) for q, d in itertools.product(queries, db) if have_intersection(q, d)}
