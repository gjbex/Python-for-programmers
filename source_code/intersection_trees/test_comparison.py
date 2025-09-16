#!/usr/bin/env python3
'''
Test script to compare the original node-based intersection tree
with the new array-based implementation to ensure they produce
identical results.
'''

import random
import time
import typing
import intersection_tree as original
import array_intersection_tree as array_based


def test_correctness(num_intervals: int = 100, num_queries: int = 50, max_end: int = 1000) -> bool:
    '''Test that both implementations produce identical results.
    
    Parameters
    ----------
    num_intervals: int
        number of intervals in the database
    num_queries: int
        number of query intervals
    max_end: int
        maximum end value for intervals
        
    Returns
    -------
    bool
        True if both implementations produce identical results
    '''
    print(f"Testing correctness with {num_intervals} intervals, {num_queries} queries...")
    
    # Generate the same set of intervals for both implementations
    random.seed(42)  # For reproducible results
    intervals = [original.generate_interval(max_end) for _ in range(num_intervals)]
    queries = [original.generate_interval(max_end) for _ in range(num_queries)]
    
    # Create databases using both implementations
    random.seed(42)
    original_db = original.populate_db(None, intervals)
    
    random.seed(42)
    array_db = array_based.populate_db(None, intervals)
    
    # Execute queries on both databases
    original_results = original.execute_queries(queries, original_db)
    array_results = array_based.execute_queries(queries, array_db)
    
    # Convert results to sets for comparison (order shouldn't matter)
    original_set = set(original_results)
    array_set = set(array_results)
    
    print(f"Original implementation found {len(original_results)} intersections")
    print(f"Array implementation found {len(array_results)} intersections")
    
    if original_set == array_set:
        print("✓ Both implementations produce identical results!")
        return True
    else:
        print("✗ Results differ between implementations!")
        print(f"Original only: {original_set - array_set}")
        print(f"Array only: {array_set - original_set}")
        return False


def benchmark_performance(sizes: list[int] = [100, 500, 1000, 2000], num_queries: int = 100) -> None:
    '''Benchmark performance of both implementations.
    
    Parameters
    ----------
    sizes: list[int]
        list of database sizes to test
    num_queries: int
        number of queries to execute for each size
    '''
    print("\nPerformance Benchmark:")
    print("Size\tOriginal (s)\tArray (s)\tSpeedup")
    print("-" * 45)
    
    for size in sizes:
        # Generate data
        random.seed(42)
        intervals = [original.generate_interval(1_000_000) for _ in range(size)]
        queries = [original.generate_interval(1_000_000) for _ in range(num_queries)]
        
        # Test original implementation
        random.seed(42)
        start_time = time.time()
        original_db = original.populate_db(None, intervals)
        original_results = original.execute_queries(queries, original_db)
        original_time = time.time() - start_time
        
        # Test array implementation
        random.seed(42)
        start_time = time.time()
        array_db = array_based.populate_db(None, intervals)
        array_results = array_based.execute_queries(queries, array_db)
        array_time = time.time() - start_time
        
        # Calculate speedup
        speedup = original_time / array_time if array_time > 0 else float('inf')
        
        print(f"{size}\t{original_time:.4f}\t\t{array_time:.4f}\t\t{speedup:.2f}x")
        
        # Verify results are still identical
        if set(original_results) != set(array_results):
            print(f"WARNING: Results differ for size {size}!")


def test_edge_cases() -> bool:
    '''Test edge cases for both implementations.
    
    Returns
    -------
    bool
        True if all edge cases pass
    '''
    print("\nTesting edge cases...")
    
    # Test invalid intervals
    try:
        original.Node((10, 10))  # start == end
        print("✗ Original implementation should reject start == end")
        return False
    except ValueError:
        print("✓ Original implementation correctly rejects start == end")
    
    try:
        tree = array_based.ArrayTree()
        tree.insert((10, 10))  # start == end
        print("✗ Array implementation should reject start == end")
        return False
    except ValueError:
        print("✓ Array implementation correctly rejects start == end")
    
    try:
        tree = array_based.ArrayTree()
        tree.insert((20, 10))  # start > end
        print("✗ Array implementation should reject start > end")
        return False
    except ValueError:
        print("✓ Array implementation correctly rejects start > end")
    
    # Test empty search
    original_tree = original.Node((10, 20))
    original_results = []
    original_tree.search((25, 30), original_results)
    
    array_tree = array_based.ArrayTree()
    array_tree.insert((10, 20))
    array_results = []
    array_tree.search((25, 30), array_results)
    
    if len(original_results) == len(array_results) == 0:
        print("✓ Both implementations handle non-intersecting queries correctly")
    else:
        print("✗ Non-intersecting query handling differs")
        return False
    
    # Test single interval intersection
    original_results = []
    original_tree.search((15, 25), original_results)
    
    array_results = []
    array_tree.search((15, 25), array_results)
    
    if len(original_results) == len(array_results) == 1:
        print("✓ Both implementations handle single intersection correctly")
    else:
        print("✗ Single intersection handling differs")
        return False
    
    return True


def main():
    '''Run all tests and benchmarks.'''
    print("Intersection Tree Implementation Comparison")
    print("=" * 50)
    
    # Test correctness
    correctness_passed = test_correctness()
    
    if correctness_passed:
        # Test edge cases
        edge_cases_passed = test_edge_cases()
        
        if edge_cases_passed:
            # Run performance benchmark
            benchmark_performance()
            print("\nAll tests passed! 🎉")
        else:
            print("\nEdge case tests failed! ❌")
    else:
        print("\nCorrectness tests failed! ❌")


if __name__ == '__main__':
    main()