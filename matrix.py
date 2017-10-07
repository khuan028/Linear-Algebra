"""
The MIT License (MIT)

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

import vector

scalarTypes = (int, float)

class Matrix(object):

    def __init__(self, args):
        self.values = [list(row) for row in args]

    @property
    def get_list(self):
        return self.values

    def __add__(self, other):
        """
        Calculates the sum of self and other

        :param other: the other matrix
        :return: the sum matrix
        """
        if type(other) == type(self):
            newMat =  [[self[row][col] + other[row][col]
                        for col in range(len(row))]
                        for row in range(len(self))]
            return Matrix(newMat)

        else:
            raise TypeError("Can only add two matrices")

    def scale(self, scalar):
        """
        Scales the matrix by a constant

        :param scalar: the scalar multiplier
        :return: the scaled matrix
        """
        if isinstance(scalar, scalarTypes):
            newMat = [[self[row][col] * scalar
                       for col in range(len(self[row]))]
                       for row in range(len(self))]
            return Matrix(newMat)

        else:
            raise TypeError("Scalar must be a constant")

    def __rmul__(self, other):
        if isinstance(other, scalarTypes):
            return self.scale(other)
        elif type(other) == type(self):
            return self._matrix_mult(other)
        else:
            raise TypeError("Multiplication only works with scalars and matrices")

    def __mul__(self, other):
        if isinstance(other, scalarTypes):
            return self.scale(other)
        elif type(other) == type(self):
            return other._matrix_mult(self)
        elif type(other) == vector.Vector:
            return other.matrix_mult(self.get_list)
        else:
            raise TypeError("Multiplication only works with scalars and matrices")

    def _matrix_mult(self, other):
        if all(len(x) == 0 for x in (self, other)):
            return Matrix([])

        if len(self) != len(other[0]):
            raise ValueError("Matrix dimensions {}x{} and {}x{} are incompatible".format(len(other), len(other[0]), len(self), len(self[0])))

        mat = [[self.col_vec(col) * other.row_vec(row)
                for col in range(len(self[0]))]
                for row in range(len(other))]
        return Matrix(mat)

    def transpose(self):
        """
        Swaps rows with columns

        :return: transposed matrix
        """
        if len(self) == 0:
            return []

        newMat = [[self[row][col]
                   for row in range(len(self))]
                   for col in range(len(self[0]))]
        return newMat

    def row_vec(self, n):
        """
        Get the nth row vector

        :param n: row index
        :return: nth row vector
        """
        return vector.Vector(*self[n])

    def col_vec(self, n):
        """
        Get the nth column vector

        :param n: column index
        :return: nth column vector
        """
        return vector.Vector(*(row[n] for row in self))

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