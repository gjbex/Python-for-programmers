'''
Module that defines a Point class representing a point in 2D space.
'''

import dataclasses
from math import sqrt
import typing


@dataclasses.dataclass
class Point:
    '''
    A class representing a point in 2D space.

    Attributes:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
    '''

    x: float
    y: float

    def distance(self, other: typing.Self) -> float:
        '''
        Calculate the Euclidean distance between this point and another point.

        Parameters:
            other (Point): The other point to which the distance is calculated.

        Returns:
            float: The Euclidean distance between the two points.
        '''
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
