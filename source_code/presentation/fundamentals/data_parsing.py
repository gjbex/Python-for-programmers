#!/usr/bin/env python
'''module to parse a line of data into its fields'''

import typing


class LineData(typing.NamedTuple):
    '''A named tuple to hold the fields of a line of data.'''
    case: int
    dim: int
    temperature: float


def parse_line(line: str) -> LineData:
    '''Split a line into its fields, convert to the appropriate types,
       and return as a tuple.
       >>> parse_line('5  3  3.7')
       (5, 3, 3.7)
       >>> parse_line('5 3 3')
       (5, 3, 3)
      '''
    data = line.rstrip('\r\n').split()
    return LineData(
               case=int(data[0]),
               dim=int(data[1]),
               temperature=float(data[2])
    )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
