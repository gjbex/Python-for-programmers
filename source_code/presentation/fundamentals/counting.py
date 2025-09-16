#!/usr/bin/env python

import sys
import data_parsing


def main():
    # read column headers
    sys.stdin.readline()
    threshold = 1.0e-7
    counter = {
        'negative': 0,
        'zero': 0,
        'positive': 0
    }
    for line in sys.stdin:
        values = data_parsing.parse_line(line)
        if values.temperature < -threshold:
            counter['negative'] += 1
        elif values.temperature > threshold:
            counter['positive'] += 1
        else:
            counter['zero'] += 1
    for key, value in counter.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
