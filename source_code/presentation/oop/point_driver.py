#!/usr/bin/env python3

from point_01 import Point


def main():
    p = Point(3, 4)
    q = Point(-2, 5)
    print(p.x, p.y)
    print(p, q)
    print(p.distance(q))
    p.x = 12.3
    print(p)


if __name__ == "__main__":
    main()
