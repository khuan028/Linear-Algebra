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
        if len(args) == 0:
            self.values = [[]]
        elif all((len(x) == len(args[0]) for x in args)):
            self.values = [list(row) for row in args]
        else:
            raise ValueError("Could not create Matrix. Matrix must be rectangular.")

    @property
    def get_list(self):
        return self.values

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

    def _matrix_mult(self, other):
        if all(len(x) == 0 for x in (self, other)):
            return Matrix([])

        if len(self) != len(other[0]):
            raise ValueError(
                "Matrix dimensions {}x{} and {}x{} are incompatible".format(len(other), len(other[0]), len(self),
                                                                            len(self[0])))

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
        return Matrix(newMat)

    def determinant(self):
        """
        Calculates the determinant

        :return: determinant
        """
        return determinant(self.values)

    def minors(self):
        """
        Calculates the matrix of minors

        :return: matrix of minors
        """
        return minors(self.values)

    def cofactors(self):
        """
        Calculates the matrix of cofactors

        :return: matrix of cofactors
        """
        return cofactors(self.values)

    def inverse(self):
        """
        Calculates the inverse matrix

        :return: inverse matrix
        """
        return inverse(self.values)

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

    def __add__(self, other):
        """
        Calculates the sum of self and other

        :param other: the other matrix
        :return: the sum matrix
        """
        if type(other) == type(self):
            if is_compatible(other, self):
                newMat = [[other[row][col] + self[row][col]
                           for col in range(len(row))]
                          for row in range(len(self))]
                return Matrix(newMat)
            else:
                raise ValueError(
                    "Matrix dimensions {}x{} and {}x{} are incompatible".format(len(other), len(other[0]), len(self),
                                                                                len(self[0])))

        else:
            raise TypeError("Can only add two matrices")

    def __sub__(self, other):
        """
        Calculates the difference of self and other

        :param other: the other matrix
        :return: the sum matrix
        """
        if type(other) == type(self):
            if is_compatible(other, self):
                newMat = [[other[row][col] - self[row][col]
                           for col in range(len(row))]
                          for row in range(len(self))]
                return Matrix(newMat)
            else:
                raise ValueError(
                    "Matrix dimensions {}x{} and {}x{} are incompatible".format(len(other), len(other[0]), len(self),
                                                                                len(self[0])))

        else:
            raise TypeError("Can only subtract two matrices")

    def __truediv__(self, other):
        if isinstance(other, scalarTypes):
            return (1 / other) * self
        else:
            raise TypeError("Can only divide by constants")

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

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __repr__(self):
        return str(self.values)

    def __str__(self):
        return "[" + "\n".join(str(row) for row in self.values) + "]"


def minors(mat):
    """
    Calculates the matrix of minors

    :param mat: input matrix
    :return: matrix of minors
    """
    minorsMat = [[determinant(sub_matrix(row, col, mat))
                  for col in range(len(mat[row]))]
                 for row in range(len(mat))]
    return Matrix(minorsMat)

def cofactors(mat):
    """
    Calculates the matrix of cofactors

    :param mat: input matrix
    :return: matrix of cofactors
    """
    minorsMat = minors(mat)
    coMat = [[(-1) ** (row + col) * minorsMat[row][col]
              for col in range(len(minorsMat[row]))]
             for row in range(len(minorsMat))]
    return Matrix(coMat)

def inverse(mat):
    """
    Calculates the inverse matrix

    :param mat: input matrix
    :return: inverse matrix
    """
    det = determinant(mat)
    if det == 0:
        raise ZeroDivisionError("This matrix has no inverse because the determinant is 0")
    else:
        coMat = cofactors(mat)
        adj = coMat.transpose()
        invMat = (1 / det) * adj
        return invMat

def determinant(mat) -> float:
    """
    Calculates the determinant

    :param mat: input matrix
    :return: determinant of input matrix
    """
    if len(mat) == len(mat[0]):
        if len(mat) == 1:
            return mat[0][0]
        else:
            x = 0
            for col in range(len(mat)):
                x += ((-1) ** col) * mat[0][col] * determinant(sub_matrix(0, col, mat))
            return x
    else:
        raise ValueError("Cannot calculate determinant. Matrix must be a square matrix.")

def sub_matrix(i, j, mat):
    """
    Creates a submatrix from mat by deleting row i and column j
    :param i: row to delete
    :param j: column to delete
    :param mat: input matrix
    :return: submatrix
    """
    sub = [[mat[row][col]
            for col in range(len(mat[row])) if col != j]
           for row in range(len(mat)) if row != i]
    return Matrix(sub)

def is_compatible(mat1, mat2):
    """
    Returns true if the two matrices can be multiplied

    :param mat1: first matrix
    :param mat2: second matrix
    :return: whether they can be multiplied or not
    """
    return len(mat1[0]) == len(mat2)