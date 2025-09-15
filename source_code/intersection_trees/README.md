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
1. `build_time_analysis.py`: comprehensive build time performance analysis.
1. `build_time_focused_analysis.py`: focused analysis answering build vs query performance questions.

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

#### Query Performance
- **Traditional (Node-based)**: ~20% faster query execution
- **Array-based**: ~20% slower query execution
- Both scale similarly with increasing dataset size

#### Build/Insertion Performance  
- **Traditional (Node-based)**: ~12% faster build time
- **Array-based**: ~12% slower build time
- Node-based achieves ~310k insertions/sec vs ~250k insertions/sec for array-based

#### Memory Usage
- **Traditional (Node-based)**: Higher memory usage (~3x more)
- **Array-based**: ~70% less memory usage
- Better cache locality potential for sequential access patterns

#### Trade-off Summary
- **Array-based**: Slower build (~12%) and query (~20%) but major memory savings (~70%)
- **Node-based**: Faster in all operations but uses significantly more memory
- **Recommendation**: Use node-based for performance-critical, use array-based for memory-constrained environments
