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

    def __init__(self):
        self._state = State.start
        self._comment_str = '#'
        self._current_block_name = None
        self._block_begin_re = re.compile(r'begin\s+block\s+(\w+)\s*$')
        self._block_end_re = re.compile(r'end\s+block\s+(\w+)\s*$')
        self._item_re = re.compile(r'item\s+(\w+)\s*$')
        self._blocks = None

    def _is_comment(self, line: str) -> bool:
        return line.startswith(self._comment_str)

    def _is_block_begin(self, line: str) -> bool:
        match = self._block_begin_re.match(line)
        if match:
            self._previous_block_name = self._current_block_name
            self._current_block_name = match.group(1)
            self._current_block = []
            return True
        return False

    def _is_block_end(self, line: str) -> bool:
        match = self._block_end_re.match(line)
        if match:
            if match.group(1) != self._current_block_name:
                raise ValueError(f'block ""{self._current_block_name}" is ended by "{match.group(1)}"')
            self._blocks[self._current_block_name] = self._current_block
            self._current_block_name = None
            self._current_block = None
            return True
        return False

    def _is_item(self, line: str) -> bool:
        match = self._item_re.match(line)
        if match:
            self._current_block.append(match.group(1))
            return True
        return False

    def parse(self, file_name: str) -> Blocks:
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
