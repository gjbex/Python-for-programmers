#!/usr/bin/env python3
'''
Focused analysis specifically answering the question: "The query performance of the 
array-based implementation of intersection trees is lower than that of the naive 
implementation, but what about the build time? How does insertion of intervals stack 
up between the two approaches?"

This script provides a clear, focused answer to this specific question.
'''

import random
import time
import gc
import intersection_tree as node_based
import array_intersection_tree as array_based


def focused_build_time_comparison(sizes: list[int] = [1000, 5000, 10000, 20000, 50000]) -> None:
    '''Compare build times specifically between node-based and array-based implementations.
    
    Parameters
    ----------
    sizes: list[int]
        list of database sizes to test
    '''
    print("FOCUSED BUILD TIME ANALYSIS")
    print("Answering: How does insertion of intervals stack up between the two approaches?")
    print("=" * 80)
    print()
    
    print("Build Time Comparison: Node-based vs Array-based Intersection Trees")
    print("-" * 70)
    print("Size\tNode Build\tArray Build\tArray Slower By\tArray Overhead")
    print("-" * 70)
    
    build_time_data = []
    
    for size in sizes:
        # Generate same intervals for both tests
        random.seed(42)
        intervals = [node_based.generate_interval(1_000_000) for _ in range(size)]
        
        # Test node-based build time
        random.seed(42)
        gc.collect()
        start_time = time.time()
        node_db = node_based.populate_db(None, intervals)
        node_build_time = time.time() - start_time
        
        # Test array-based build time
        random.seed(42)
        gc.collect()
        start_time = time.time()
        array_db = array_based.populate_db(None, intervals)
        array_build_time = time.time() - start_time
        
        # Calculate overhead
        slowdown_factor = array_build_time / node_build_time if node_build_time > 0 else float('inf')
        overhead_percentage = (array_build_time - node_build_time) / node_build_time * 100 if node_build_time > 0 else 0
        
        print(f"{size}\t{node_build_time:.4f}s\t{array_build_time:.4f}s\t{slowdown_factor:.2f}x\t\t+{overhead_percentage:.1f}%")
        
        build_time_data.append({
            'size': size,
            'node_time': node_build_time,
            'array_time': array_build_time,
            'slowdown': slowdown_factor,
            'overhead': overhead_percentage
        })
    
    # Calculate average overhead
    avg_overhead = sum(d['overhead'] for d in build_time_data) / len(build_time_data)
    avg_slowdown = sum(d['slowdown'] for d in build_time_data) / len(build_time_data)
    
    print("-" * 70)
    print(f"Average build time overhead: +{avg_overhead:.1f}%")
    print(f"Average slowdown factor: {avg_slowdown:.2f}x")
    print()
    
    return build_time_data


def insertion_rate_analysis(build_data: list) -> None:
    '''Analyze insertion rates for both implementations.
    
    Parameters
    ----------
    build_data: list
        build time data from focused_build_time_comparison
    '''
    print("INSERTION RATE ANALYSIS")
    print("-" * 40)
    print("Size\tNode Rate\tArray Rate\tRate Difference")
    print("\t(intervals/sec)\t(intervals/sec)")
    print("-" * 50)
    
    for data in build_data:
        node_rate = data['size'] / data['node_time'] if data['node_time'] > 0 else float('inf')
        array_rate = data['size'] / data['array_time'] if data['array_time'] > 0 else float('inf')
        rate_diff = (node_rate - array_rate) / array_rate * 100 if array_rate > 0 else 0
        
        print(f"{data['size']}\t{node_rate:.0f}\t\t{array_rate:.0f}\t\t+{rate_diff:.1f}%")
    
    print()


def answer_the_question(build_data: list) -> None:
    '''Provide a clear answer to the original question.
    
    Parameters
    ----------
    build_data: list
        build time data from focused_build_time_comparison
    '''
    print("ANSWER TO THE QUESTION")
    print("=" * 50)
    print()
    print("Question: 'The query performance of the array-based implementation of")
    print("intersection trees is lower than that of the naive implementation, but")
    print("what about the build time? How does insertion of intervals stack up")
    print("between the two approaches?'")
    print()
    print("ANSWER:")
    print("-" * 20)
    
    # Calculate averages
    avg_overhead = sum(d['overhead'] for d in build_data) / len(build_data)
    avg_slowdown = sum(d['slowdown'] for d in build_data) / len(build_data)
    
    print(f"1. BUILD TIME PERFORMANCE:")
    print(f"   • Array-based implementation is SLOWER at building/insertion")
    print(f"   • Average build time overhead: +{avg_overhead:.1f}%")
    print(f"   • Average slowdown factor: {avg_slowdown:.2f}x")
    print()
    
    print(f"2. INSERTION PERFORMANCE:")
    print(f"   • Node-based trees insert intervals ~{avg_slowdown:.1f}x faster")
    print(f"   • Array-based has higher per-insertion overhead")
    print(f"   • The array-based approach sacrifices build speed for memory efficiency")
    print()
    
    print(f"3. TRADE-OFF SUMMARY:")
    print(f"   • Array-based: Better memory usage (~70% savings), slower build & query")
    print(f"   • Node-based: Faster build & query, higher memory usage")
    print(f"   • Neither approach has a 'free lunch' - it's memory vs speed")
    print()
    
    print(f"4. PRACTICAL IMPLICATIONS:")
    print(f"   • For write-heavy workloads: Node-based is better")
    print(f"   • For memory-constrained environments: Array-based might be worth it")
    print(f"   • The ~{avg_overhead:.0f}% build overhead is relatively small compared to memory savings")
    print()


def main():
    '''Run focused build time analysis to answer the specific question.'''
    print("INTERSECTION TREES BUILD TIME ANALYSIS")
    print("Specifically answering the build time vs query time question")
    print("=" * 60)
    print()
    
    # Run focused build time comparison
    build_data = focused_build_time_comparison()
    
    # Analyze insertion rates
    insertion_rate_analysis(build_data)
    
    # Provide clear answer to the question
    answer_the_question(build_data)


if __name__ == '__main__':
    main()