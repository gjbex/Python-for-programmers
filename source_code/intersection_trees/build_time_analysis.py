#!/usr/bin/env python3
'''
Focused analysis of build time performance comparing node-based and array-based
intersection tree implementations. This script specifically addresses the question:
"The query performance of the array-based implementation is lower than that of the 
naive implementation, but what about the build time? How does insertion of intervals 
stack up between the two approaches?"
'''

import random
import time
import typing
import gc
import intersection_tree as node_based
import array_intersection_tree as array_based
import naive_intersectionic_queries as naive


def time_build_process(intervals: list[tuple[int, int]], implementation: str) -> tuple[float, float]:
    '''Time the build process for a given implementation.
    
    Parameters
    ----------
    intervals: list[tuple[int, int]]
        list of intervals to insert
    implementation: str
        either 'node', 'array', or 'naive'
        
    Returns
    -------
    tuple[float, float]
        (total_build_time, average_insertion_time)
    '''
    gc.collect()  # Clean up before timing
    
    if implementation == 'node':
        start_time = time.time()
        db = node_based.populate_db(None, intervals)
        build_time = time.time() - start_time
        
    elif implementation == 'array':
        start_time = time.time()
        db = array_based.populate_db(None, intervals)
        build_time = time.time() - start_time
        
    elif implementation == 'naive':
        start_time = time.time()
        db = naive.create_db(len(intervals))  # Naive doesn't have populate_db
        build_time = time.time() - start_time
        
    else:
        raise ValueError(f"Unknown implementation: {implementation}")
    
    avg_insertion_time = build_time / len(intervals) if intervals else 0
    return build_time, avg_insertion_time


def incremental_insertion_test(max_size: int = 10000, step: int = 1000) -> None:
    '''Test incremental insertion performance.
    
    Parameters
    ----------
    max_size: int
        maximum number of intervals to test
    step: int
        step size for increasing interval count
    '''
    print("Incremental Insertion Performance Test")
    print("=" * 60)
    print("Size\tNode Build\tArray Build\tNaive Build\tNode/Array\tNode/Naive\tArray/Naive")
    print("-" * 95)
    
    sizes = list(range(step, max_size + 1, step))
    
    for size in sizes:
        # Generate same intervals for all tests
        random.seed(42)
        intervals = [node_based.generate_interval(1_000_000) for _ in range(size)]
        
        # Test node-based implementation
        random.seed(42)
        node_build_time, node_avg = time_build_process(intervals, 'node')
        
        # Test array-based implementation  
        random.seed(42)
        array_build_time, array_avg = time_build_process(intervals, 'array')
        
        # Test naive implementation
        random.seed(42)
        naive_build_time, naive_avg = time_build_process(intervals, 'naive')
        
        # Calculate ratios
        node_array_ratio = node_build_time / array_build_time if array_build_time > 0 else float('inf')
        node_naive_ratio = node_build_time / naive_build_time if naive_build_time > 0 else float('inf')
        array_naive_ratio = array_build_time / naive_build_time if naive_build_time > 0 else float('inf')
        
        print(f"{size}\t{node_build_time:.4f}s\t{array_build_time:.4f}s\t{naive_build_time:.4f}s\t{node_array_ratio:.2f}x\t{node_naive_ratio:.2f}x\t{array_naive_ratio:.2f}x")


def single_insertion_timing_test(num_trials: int = 1000) -> None:
    '''Test individual insertion timing.
    
    Parameters
    ----------
    num_trials: int
        number of insertion operations to time
    '''
    print(f"\nSingle Insertion Timing Test ({num_trials} trials)")
    print("=" * 50)
    
    # Prepare intervals
    random.seed(42)
    intervals = [node_based.generate_interval(1_000_000) for _ in range(num_trials)]
    
    # Test node-based individual insertions
    node_tree = node_based.Node(intervals[0])
    gc.collect()
    
    start_time = time.time()
    for interval in intervals[1:]:
        node_tree.insert(interval)
    node_insertion_time = time.time() - start_time
    
    # Test array-based individual insertions
    array_tree = array_based.ArrayTree()
    array_tree.insert(intervals[0])
    gc.collect()
    
    start_time = time.time()
    for interval in intervals[1:]:
        array_tree.insert(interval)
    array_insertion_time = time.time() - start_time
    
    node_avg = node_insertion_time / (num_trials - 1)
    array_avg = array_insertion_time / (num_trials - 1)
    speedup = node_insertion_time / array_insertion_time if array_insertion_time > 0 else float('inf')
    
    print(f"Node-based total time: {node_insertion_time:.4f}s")
    print(f"Array-based total time: {array_insertion_time:.4f}s")
    print(f"Node-based avg per insertion: {node_avg*1000:.3f} ms")
    print(f"Array-based avg per insertion: {array_avg*1000:.3f} ms")
    print(f"Insertion speedup (Node/Array): {speedup:.2f}x")


def memory_efficiency_during_build(sizes: list[int] = [1000, 5000, 10000]) -> None:
    '''Analyze memory efficiency during the build process.
    
    Parameters
    ----------
    sizes: list[int]
        list of database sizes to test
    '''
    print(f"\nMemory Efficiency During Build")
    print("=" * 40)
    print("Size\tNode Memory\tArray Memory\tSavings\tNode Build\tArray Build\tMem/Time Ratio")
    print("-" * 85)
    
    import sys
    
    for size in sizes:
        # Generate intervals
        random.seed(42)
        intervals = [node_based.generate_interval(1_000_000) for _ in range(size)]
        
        # Build and measure node-based
        random.seed(42)
        gc.collect()
        start_time = time.time()
        node_db = node_based.populate_db(None, intervals)
        node_build_time = time.time() - start_time
        
        # Estimate node memory (rough approximation)
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
        
        node_memory = estimate_tree_size(node_db)
        
        # Build and measure array-based
        random.seed(42)
        gc.collect()
        start_time = time.time()
        array_db = array_based.populate_db(None, intervals)
        array_build_time = time.time() - start_time
        
        array_memory = (
            sys.getsizeof(array_db.start) +
            sys.getsizeof(array_db.end) +
            sys.getsizeof(array_db.max_end) +
            sys.getsizeof(array_db.left) +
            sys.getsizeof(array_db.right) +
            sys.getsizeof(array_db)
        )
        
        savings = (node_memory - array_memory) / node_memory * 100 if node_memory > 0 else 0
        mem_time_ratio_node = node_memory / node_build_time if node_build_time > 0 else float('inf')
        mem_time_ratio_array = array_memory / array_build_time if array_build_time > 0 else float('inf')
        ratio_improvement = mem_time_ratio_node / mem_time_ratio_array if mem_time_ratio_array > 0 else float('inf')
        
        print(f"{size}\t{node_memory/1024:.0f} KB\t{array_memory/1024:.0f} KB\t{savings:.1f}%\t{node_build_time:.4f}s\t{array_build_time:.4f}s\t{ratio_improvement:.2f}x")


def build_vs_query_tradeoff_analysis(sizes: list[int] = [1000, 5000, 10000], num_queries: int = 100) -> None:
    '''Analyze the tradeoff between build time and query time.
    
    Parameters
    ----------
    sizes: list[int]
        list of database sizes to test
    num_queries: int
        number of queries to execute
    '''
    print(f"\nBuild vs Query Performance Tradeoff Analysis")
    print("=" * 60)
    print("Size\tNode Build\tArray Build\tNode Query\tArray Query\tBuild Advantage\tQuery Disadvantage")
    print("-" * 95)
    
    for size in sizes:
        # Generate test data
        random.seed(42)
        intervals = [node_based.generate_interval(1_000_000) for _ in range(size)]
        queries = [node_based.generate_interval(1_000_000) for _ in range(num_queries)]
        
        # Node-based timing
        random.seed(42)
        node_build_time, _ = time_build_process(intervals, 'node')
        
        node_db = node_based.populate_db(None, intervals)
        gc.collect()
        start_time = time.time()
        node_based.execute_queries(queries, node_db)
        node_query_time = time.time() - start_time
        
        # Array-based timing
        random.seed(42)
        array_build_time, _ = time_build_process(intervals, 'array')
        
        array_db = array_based.populate_db(None, intervals)
        gc.collect()
        start_time = time.time()
        array_based.execute_queries(queries, array_db)
        array_query_time = time.time() - start_time
        
        # Calculate advantages/disadvantages
        build_advantage = (array_build_time - node_build_time) / node_build_time * 100 if node_build_time > 0 else 0
        query_disadvantage = (array_query_time - node_query_time) / node_query_time * 100 if node_query_time > 0 else 0
        
        print(f"{size}\t{node_build_time:.4f}s\t{array_build_time:.4f}s\t{node_query_time:.4f}s\t{array_query_time:.4f}s\t{build_advantage:+.1f}%\t{query_disadvantage:+.1f}%")


def main():
    '''Run focused build time performance analysis.'''
    print("Build Time Performance Analysis")
    print("Comparing Node-based vs Array-based Intersection Trees")
    print("=" * 70)
    
    # Run incremental insertion test
    incremental_insertion_test(max_size=10000, step=1000)
    
    # Run single insertion timing
    single_insertion_timing_test(num_trials=1000)
    
    # Run memory efficiency analysis
    memory_efficiency_during_build()
    
    # Run build vs query tradeoff analysis
    build_vs_query_tradeoff_analysis()
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("- Array-based implementation may have different build time characteristics")
    print("- Individual insertion performance comparison completed")
    print("- Memory efficiency during build process analyzed")
    print("- Build vs Query performance tradeoff quantified")
    print("=" * 70)


if __name__ == '__main__':
    main()