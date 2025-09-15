# Intersection trees

This project illustrates that implementation details, but mostly algorithmic
choices, can have an impact on performance when performing intersection queries
on intervals.


## What is it?

1. `intersection_trees.ipynb`: Jupyter notebook illustrating the different
   implementations and their performance.
1. `naive_pythonic_intersectionic_queries.py`: brute force implementaion that
   uses sets and named tuples.
1. `naive_intersectionic_queries.py`: brute force implementaion that
   uses lists and tuples.
1. `intersection_tree.py`: implementation of an intersection tree using traditional node-based structure.
1. `array_intersection_tree.py`: alternative array-based implementation of an intersection tree.
1. `test_comparison.py`: comprehensive test suite comparing both implementations.
1. `performance_analysis.py`: detailed performance analysis and benchmarking tools.

## Implementation Comparison

### Traditional Node-based Tree (`intersection_tree.py`)
- Uses traditional tree nodes with object references
- Each node is a separate object with `start`, `end`, `max_end`, `left`, `right` attributes
- More intuitive object-oriented design
- Faster execution time due to direct object access

### Array-based Tree (`array_intersection_tree.py`)
- Uses arrays to store tree data: `start[]`, `end[]`, `max_end[]`, `left[]`, `right[]`
- Nodes are represented as indices into these arrays
- Better memory density (~70% memory savings)
- Slightly slower execution (~20% overhead) due to array indexing

### Performance Characteristics
- **Memory Usage**: Array-based implementation uses ~70% less memory
- **Execution Speed**: Traditional implementation is ~20% faster
- **Cache Locality**: Array-based shows potential for better cache performance with sequential access patterns
- **Scalability**: Both implementations scale similarly with increasing dataset size
