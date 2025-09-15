#!/usr/bin/env python3
'''
Demo script showing both intersection tree implementations
'''

import intersection_tree as original
import array_intersection_tree as array_based


def demo_basic_usage():
    '''Demonstrate basic usage of both implementations.'''
    print("=== Basic Usage Demo ===")
    print()
    
    # Create some sample intervals
    intervals = [(10, 30), (20, 40), (50, 70), (60, 80), (5, 15)]
    query = (25, 55)
    
    print(f"Sample intervals: {intervals}")
    print(f"Query interval: {query}")
    print()
    
    # Original implementation
    print("Original Node-based Implementation:")
    original_tree = original.populate_db(None, intervals)
    original_results = []
    original_tree.search(query, original_results)
    print(f"  Found {len(original_results)} intersections: {original_results}")
    print(f"  Tree structure:")
    print(f"    {original_tree.to_str().replace(chr(10), chr(10) + '    ')}")
    
    # Array-based implementation
    print("Array-based Implementation:")
    array_tree = array_based.populate_db(None, intervals)
    array_results = []
    array_tree.search(query, array_results)
    print(f"  Found {len(array_results)} intersections: {array_results}")
    print(f"  Tree structure:")
    print(f"    {array_tree.to_str().replace(chr(10), chr(10) + '    ')}")
    
    # Verify results match
    print(f"Results match: {set(original_results) == set(array_results)}")


def demo_performance():
    '''Demonstrate performance characteristics.'''
    print("\n=== Performance Demo ===")
    print()
    
    import time
    import random
    
    # Test with different sizes
    sizes = [1000, 5000, 10000]
    
    print("Performance comparison (build + 100 queries):")
    print("Size\tOriginal\tArray\t\tMemory Savings")
    print("-" * 50)
    
    for size in sizes:
        # Generate data
        random.seed(42)
        intervals = [original.generate_interval(1_000_000) for _ in range(size)]
        queries = [original.generate_interval(1_000_000) for _ in range(100)]
        
        # Original implementation
        random.seed(42)
        start = time.time()
        orig_db = original.populate_db(None, intervals)
        original.execute_queries(queries, orig_db)
        orig_time = time.time() - start
        
        # Array implementation
        random.seed(42)
        start = time.time()
        array_db = array_based.populate_db(None, intervals)
        array_based.execute_queries(queries, array_db)
        array_time = time.time() - start
        
        # Estimate memory usage (rough approximation)
        import sys
        orig_mem = size * (sys.getsizeof(0) * 5 + sys.getsizeof(object()) * 2)  # approximation
        array_mem = array_db._capacity * sys.getsizeof(0) * 5  # 5 arrays
        mem_savings = (orig_mem - array_mem) / orig_mem * 100
        
        print(f"{size}\t{orig_time:.3f}s\t\t{array_time:.3f}s\t\t~{mem_savings:.0f}%")


def demo_visualization():
    '''Demonstrate visualization capabilities.'''
    print("\n=== Visualization Demo ===")
    print()
    
    # Create a small tree for visualization
    intervals = [(10, 30), (5, 15), (25, 45), (35, 55)]
    
    print("Creating visualization for small tree...")
    print("(Note: Requires matplotlib to be installed)")
    
    try:
        import matplotlib.pyplot as plt
        
        # Original tree
        orig_tree = original.populate_db(None, intervals)
        print("Displaying original tree...")
        original.plot_intersection_tree(orig_tree)
        
        # Array tree
        array_tree = array_based.populate_db(None, intervals)
        print("Displaying array-based tree...")
        array_based.plot_intersection_tree(array_tree)
        
    except ImportError:
        print("matplotlib not available - skipping visualization")
        print("Install with: pip install matplotlib")


def main():
    '''Run all demos.'''
    print("Intersection Tree Implementation Demo")
    print("=" * 40)
    
    demo_basic_usage()
    demo_performance()
    demo_visualization()
    
    print("\nDemo complete!")


if __name__ == '__main__':
    main()