# Parser

This is an illustration of a parser implemented as a finite-state machine
(FSM).  The states of the parser are represented as Python `enum.Enum` members,
and the transitions between are implemented using a `match` statement.


## What is it?

1. `parser.ipynb`: A Jupyter notebook that demonstrates the parser FSM.
1. `block_parser.py`: Python module containing the parser implementation.
1. `test_parser.py`: Unit tests for the parser using `pytest`.
1. `data/`: Directory containing sample input files for testing the parser.
