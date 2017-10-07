""" 
The MIT License (MIT)

Copyright (c) 2015 Mat Leonard
Copyright (c) 2017 Kevin Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import math
from collections import Sequence
import numbers
from numbers import Real, Number

class Vector(object):
    def __init__(self, *args):
        """ Create a vector, example: v = Vector(1,2) """
        if len(args) == 0:
            self.values = (0, 0)
        else:
            self.values = args

    def norm(self):
        """ Returns the norm (length, magnitude) of the vector """
        return math.sqrt(sum(comp ** 2 for comp in self))

    def argument(self):
        """ Returns the argument of the vector, the angle clockwise from +y."""
        arg_in_rad = math.acos(Vector(0, 1) * self / self.norm())
        arg_in_deg = math.degrees(arg_in_rad)
        if self.values[0] < 0:
            return 360 - arg_in_deg
        else:
            return arg_in_deg

    def normalized(self):
        """ Returns a normalized unit vector """
        norm = self.norm()
        normed = tuple(comp / norm for comp in self)
        return Vector(*normed)

    def rotated(self, *args):
        """ Rotate this vector. If passed a number, assumes this is a 
            2D vector and rotates by the passed value in degrees.  Otherwise,
            assumes the passed value is a list acting as a matrix which rotates the vector.
        """
        if len(args) == 1 and type(args[0]) == type(1) or type(args[0]) == type(1.):
            # So, if rotate is passed an int or a float...
            if len(self) != 2:
                raise ValueError("Rotation axis not defined for greater than 2D vector")
            return self._rotated2D(*args)
        elif len(args) == 1:
            matrix = args[0]
            if not all(len(row) == len(v) for row in matrix) or not len(matrix) == len(self):
                raise ValueError("Rotation matrix must be square and same dimensions as vector")
            return self.matrix_mult(matrix)

    def _rotated2D(self, theta: Real):
        """ Rotate this vector by theta in degrees.

            Returns a new vector.
        """
        theta = math.radians(theta)
        # Just applying the 2D rotation matrix
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc * x - ds * y, ds * x + dc * y
        return Vector(x, y)

    def matrix_mult(self, matrix):
        """ Multiply this vector by a matrix.  Assuming matrix is a list of lists.

            Example:
            mat = [[1,2,3],[-1,0,1],[3,4,5]]
            Vector(1,2,3).matrix_mult(mat) ->  (14, 2, 26)

        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions')

            # Grab a row from the matrix, make it a Vector, take the dot product,
        # and store it as the first component
        product = tuple(Vector(*row) * self for row in matrix)

        return Vector(*product)

    def inner(self, other):
        """ Returns the dot product (inner product) of self and other vector
        """
        return sum(a * b for a, b in zip(self, other))

    def __mul__(self, other):
        """ Returns the dot product of self and other if multiplied
            by another Vector.  If multiplied by an int or float,
            multiplies each component by other.
        """
        if type(other) == type(self):
            return self.inner(other)
        elif isinstance(other, numbers.Number):
            product = tuple(a * other for a in self)
            return Vector(*product)
        elif isinstance(other, Sequence) and isinstance(other[0], Sequence):
            raise TypeError("Matrix must be multiplied on the left")
        else:
            raise TypeError("Incompatible vector multiplication")

    def __rmul__(self, other):
        """ Performs scalar/matrix multiplication on the left
            (e.g. scalar * vec)
            (e.g. matrix * vec)
        """
        if isinstance(other, Number):
            return self.__mul__(other)
        elif isinstance(other, Sequence) and isinstance(other[0], Sequence):
            return self.matrix_mult(other)
        else:
            raise TypeError("A vector can only be multiplied by a scalar, matrix, or vector")

    def __div__(self, other: Number):
        """ Returns a vector scaled by 1 / other"""
        if isinstance(other, Number):
            divided = tuple(a / other for a in self)
            return Vector(*divided)

    def __add__(self, other):
        """ Returns the vector sum of self and other """
        added = tuple(a + b for a, b in zip(self, other))
        return Vector(*added)

    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        subbed = tuple(a - b for a, b in zip(self, other))
        return Vector(*subbed)

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __repr__(self):
        return str(self.values)

    def __str__(self):
        return str(self.values)


def cross_product(u: Vector, v: Vector):
    """
    Calculates the vector product of two vectors

    :rtype: numbers.Number
    :param u: first vector
    :param v: second vector
    :return: cross product of u and v
    """
    if all(len(x) == 3 for x in (u, v)):
        a1 = u[1] * v[2] - u[2] * v[1]
        a2 = u[2] * v[0] - u[0] * v[2]
        a3 = u[0] * v[1] - u[1] * v[0]
        return Vector(a1, a2, a3)
    else:
        raise ValueError("Vectors must be three-dimensional")


def dot_product(u: Vector, v: Vector):
    """
    Calculates the dot product of two vectors

    :rtype: numbers.Number
    :param u: first vector
    :param v: second vector
    :return: dot product of u and v
    """
    return sum(a * b for a, b in zip(u, v))
