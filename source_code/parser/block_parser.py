#!/usr/bin/env python

import enum
import re
import typing


class State(enum.Enum):
    start = enum.auto()
    in_block = enum.auto()
    not_in_block = enum.auto()


Item: typing.TypeAlias = str
Block: typing.TypeAlias = list[Item]
Blocks: typing.TypeAlias = dict[str, Block]


class Parser:
    """Parse block-formatted files into named blocks.

    Notes
    -----
    The parser enforces a grammar composed of ``begin block``/``end block``
    markers around ``item`` statements.
    """

    def __init__(self):
        """Initialize parser instance state.

        Notes
        -----
        Resets the parser to the initial state with no active block.
        """
        self._state = State.start
        self._comment_str = '#'
        self._current_block_name = None
        self._block_begin_re = re.compile(r'begin\s+block\s+(\w+)\s*$')
        self._block_end_re = re.compile(r'end\s+block\s+(\w+)\s*$')
        self._item_re = re.compile(r'item\s+(\w+)\s*$')
        self._blocks = None

    def _is_comment(self, line: str) -> bool:
        """Check whether a stripped line is a comment.

        Parameters
        ----------
        line : str
            Input line stripped of surrounding whitespace.

        Returns
        -------
        bool
            True if the line begins with the comment prefix.
        """
        return line.startswith(self._comment_str)

    def _is_block_begin(self, line: str) -> bool:
        """Detect the start of a new block and prepare block state.

        Parameters
        ----------
        line : str
            Current line stripped of whitespace.

        Returns
        -------
        bool
            True when the line marks the beginning of a block.
        """
        if match := self._block_begin_re.match(line):
            self._current_block_name = match.group(1)
            self._current_block = []
            return True
        return False

    def _is_block_end(self, line: str) -> bool:
        """Detect the end of the current block and persist its items.

        Parameters
        ----------
        line : str
            Current line stripped of whitespace.

        Returns
        -------
        bool
            True when the line closes the current block.

        Raises
        ------
        ValueError
            If the closing block name does not match the active block.
        """
        if match := self._block_end_re.match(line):
            if match.group(1) != self._current_block_name:
                raise ValueError(f'block "{self._current_block_name}" is ended by "{match.group(1)}"')
            self._blocks[self._current_block_name] = self._current_block
            self._current_block_name = None
            self._current_block = None
            return True
        return False

    def _is_item(self, line: str) -> bool:
        """Detect an item entry and append it to the active block.

        Parameters
        ----------
        line : str
            Current line stripped of whitespace.

        Returns
        -------
        bool
            True when the line contains a valid item.
        """
        if match := self._item_re.match(line):
            self._current_block.append(match.group(1))
            return True
        return False

    def parse(self, file_name: str) -> Blocks:
        """Parse a block-formatted text file into named collections.

        Parameters
        ----------
        file_name : str
            Path to the file to parse.

        Returns
        -------
        Blocks
            Mapping of block names to lists of item strings.

        Raises
        ------
        ValueError
            If the input deviates from the expected block grammar.
        """
        self._blocks = {}
        line_nr: int = 0
        with open(file_name) as file:
            for line in file:
                line_nr += 1
                line = line.strip()
                # skip comments and empty lines
                if not line or self._is_comment(line):
                    continue
                match self._state:
                    case State.start:
                        if self._is_block_begin(line):
                            self._state = State.in_block
                        else:
                            raise ValueError(f'line {line_nr}: expecting begin block, got "{line}"')
                    case State.in_block:
                        if self._is_item(line):
                            pass
                        elif self._is_block_end(line):
                            self._state = State.not_in_block
                        else:
                            raise ValueError(f'line {line_nr}: expected item or end block, got "{line}"')
                    case State.not_in_block:
                        if self._is_block_begin(line):
                            self._state = State.in_block
                        else:
                            raise ValueError(f'line {line_nr}: expected begin block, got "{line}"')
        if self._state is State.in_block:
            raise ValueError(f'block "{self._current_block_name}" not ended at end of file')
        return self._blocks
