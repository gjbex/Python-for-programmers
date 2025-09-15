#!/usr/bin/env python3
'''
Comprehensive performance analysis comparing the original node-based 
intersection tree with the new array-based implementation across 
different scenarios.
'''

import random
import time
import typing
import gc
import sys
import intersection_tree as original
import array_intersection_tree as array_based


def memory_usage_comparison(sizes: list[int] = [1000, 5000, 10000, 20000]) -> None:
    '''Compare memory usage of both implementations.
    
    Parameters
    ----------
    sizes: list[int]
        list of database sizes to test
    '''
    print("Memory Usage Comparison:")
    print("Size\tOriginal (MB)\tArray (MB)\tSavings")
    print("-" * 45)
    
    for size in sizes:
        # Force garbage collection before measurements
        gc.collect()
        
        # Generate intervals
        random.seed(42)
        intervals = [original.generate_interval(1_000_000) for _ in range(size)]
        
        # Measure original implementation
        random.seed(42)
        original_db = original.populate_db(None, intervals)
        original_size = sys.getsizeof(original_db)
        
        # Rough estimation by traversing the tree (this is approximation)
        def estimate_tree_size(node):
            if node is None:
                return 0
            size = sys.getsizeof(node)
            size += sys.getsizeof(node._start) + sys.getsizeof(node._end) + sys.getsizeof(node._max_end)
            if hasattr(node, '_left') and node._left:
                size += estimate_tree_size(node._left)
            if hasattr(node, '_right') and node._right:
                size += estimate_tree_size(node._right)
            return size
        
        original_total = estimate_tree_size(original_db)
        
        # Measure array implementation
        random.seed(42)
        array_db = array_based.populate_db(None, intervals)
        array_size = (
            sys.getsizeof(array_db.start) +
            sys.getsizeof(array_db.end) +
            sys.getsizeof(array_db.max_end) +
            sys.getsizeof(array_db.left) +
            sys.getsizeof(array_db.right) +
            sys.getsizeof(array_db)
        )
        
        original_mb = original_total / (1024 * 1024)
        array_mb = array_size / (1024 * 1024)
        savings = (original_total - array_size) / original_total * 100 if original_total > 0 else 0
        
        print(f"{size}\t{original_mb:.2f}\t\t{array_mb:.2f}\t\t{savings:.1f}%")


def detailed_benchmark(sizes: list[int] = [1000, 5000, 10000, 20000, 50000], 
                      num_queries: int = 1000) -> None:
    '''Detailed performance benchmark with larger datasets.
    
    Parameters
    ----------
    sizes: list[int]
        list of database sizes to test
    num_queries: int
        number of queries to execute for each size
    '''
    print("\nDetailed Performance Benchmark:")
    print("Size\tOriginal\tArray\t\tSpeedup\tQueries/sec (Original)\tQueries/sec (Array)")
    print("-" * 90)
    
    for size in sizes:
        # Generate data
        random.seed(42)
        intervals = [original.generate_interval(10_000_000) for _ in range(size)]
        queries = [original.generate_interval(10_000_000) for _ in range(num_queries)]
        
        # Test original implementation
        random.seed(42)
        gc.collect()
        start_time = time.time()
        original_db = original.populate_db(None, intervals)
        build_time_orig = time.time() - start_time
        
        start_time = time.time()
        original_results = original.execute_queries(queries, original_db)
        query_time_orig = time.time() - start_time
        total_time_orig = build_time_orig + query_time_orig
        
        # Test array implementation
        random.seed(42)
        gc.collect()
        start_time = time.time()
        array_db = array_based.populate_db(None, intervals)
        build_time_array = time.time() - start_time
        
        start_time = time.time()
        array_results = array_based.execute_queries(queries, array_db)
        query_time_array = time.time() - start_time
        total_time_array = build_time_array + query_time_array
        
        # Calculate metrics
        speedup = total_time_orig / total_time_array if total_time_array > 0 else float('inf')
        qps_orig = num_queries / query_time_orig if query_time_orig > 0 else float('inf')
        qps_array = num_queries / query_time_array if query_time_array > 0 else float('inf')
        
        print(f"{size}\t{total_time_orig:.4f}s\t{total_time_array:.4f}s\t\t{speedup:.2f}x\t{qps_orig:.0f}\t\t\t{qps_array:.0f}")
        
        # Verify results are still identical
        if set(original_results) != set(array_results):
            print(f"WARNING: Results differ for size {size}!")


def scalability_test(max_size: int = 100000, step: int = 10000) -> None:
    '''Test scalability by gradually increasing the database size.
    
    Parameters
    ----------
    max_size: int
        maximum database size to test
    step: int
        step size for increasing database size
    '''
    print(f"\nScalability Test (up to {max_size} intervals):")
    print("Size\tOriginal Build\tArray Build\tOriginal Query\tArray Query\tTotal Speedup")
    print("-" * 80)
    
    sizes = list(range(step, max_size + 1, step))
    num_queries = 100
    
    for size in sizes:
        if size > 50000:  # Skip very large sizes for time
            break
            
        # Generate data
        random.seed(42)
        intervals = [original.generate_interval(10_000_000) for _ in range(size)]
        queries = [original.generate_interval(10_000_000) for _ in range(num_queries)]
        
        # Test original implementation
        random.seed(42)
        gc.collect()
        
        start_time = time.time()
        original_db = original.populate_db(None, intervals)
        orig_build = time.time() - start_time
        
        start_time = time.time()
        original.execute_queries(queries, original_db)
        orig_query = time.time() - start_time
        
        # Test array implementation
        random.seed(42)
        gc.collect()
        
        start_time = time.time()
        array_db = array_based.populate_db(None, intervals)
        array_build = time.time() - start_time
        
        start_time = time.time()
        array_based.execute_queries(queries, array_db)
        array_query = time.time() - start_time
        
        total_speedup = (orig_build + orig_query) / (array_build + array_query)
        
        print(f"{size}\t{orig_build:.4f}s\t\t{array_build:.4f}s\t\t{orig_query:.4f}s\t\t{array_query:.4f}s\t\t{total_speedup:.2f}x")


def cache_locality_test() -> None:
    '''Test the impact of cache locality by measuring performance with different access patterns.'''
    print("\nCache Locality Test:")
    print("Testing with sequential vs random query patterns...")
    
    size = 10000
    num_queries = 1000
    
    # Generate database
    random.seed(42)
    intervals = [original.generate_interval(1_000_000) for _ in range(size)]
    
    # Create databases
    random.seed(42)
    original_db = original.populate_db(None, intervals)
    random.seed(42)
    array_db = array_based.populate_db(None, intervals)
    
    # Test with sequential queries
    sequential_queries = [(i * 100, (i + 1) * 100) for i in range(num_queries)]
    
    start_time = time.time()
    original.execute_queries(sequential_queries, original_db)
    orig_sequential = time.time() - start_time
    
    start_time = time.time()
    array_based.execute_queries(sequential_queries, array_db)
    array_sequential = time.time() - start_time
    
    # Test with random queries
    random.seed(123)
    random_queries = [original.generate_interval(1_000_000) for _ in range(num_queries)]
    
    start_time = time.time()
    original.execute_queries(random_queries, original_db)
    orig_random = time.time() - start_time
    
    start_time = time.time()
    array_based.execute_queries(random_queries, array_db)
    array_random = time.time() - start_time
    
    print(f"Sequential queries:")
    print(f"  Original: {orig_sequential:.4f}s")
    print(f"  Array:    {array_sequential:.4f}s")
    print(f"  Speedup:  {orig_sequential/array_sequential:.2f}x")
    
    print(f"Random queries:")
    print(f"  Original: {orig_random:.4f}s")
    print(f"  Array:    {array_random:.4f}s")
    print(f"  Speedup:  {orig_random/array_random:.2f}x")


def main():
    '''Run comprehensive performance analysis.'''
    print("Comprehensive Performance Analysis")
    print("=" * 50)
    
    # Memory usage comparison
    memory_usage_comparison()
    
    # Detailed benchmark
    detailed_benchmark()
    
    # Scalability test
    scalability_test()
    
    # Cache locality test
    cache_locality_test()
    
    print("\nPerformance analysis complete!")


if __name__ == '__main__':
    main()