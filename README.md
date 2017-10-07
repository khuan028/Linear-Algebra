# LinearAlgebra
This Linear Algebra repository contains useful classes for creating and manipulating vectors and matrices.

A majority of the vector class was developed by Mat Leonard (2015). Please thank him for his GitHub gist here: https://gist.github.com/mcleonard/5351452

I made a few improvements upon Mat's code, including cross product and matrix multiplication using the * operator.


## Features:
1. Vector addition and scalar multiplication
```python
a = Vector(1,2,5,0,3)
b = Vector(10,7,4,1,1)
c = a + b
d = 3.14 * b
```
2. Magnitude and argument
```python
a = Vector(1,4)
x = a.norm()
y = a.argument()
```

3. Dot product and cross product
```python
a = Vector(5,2,7)
b = Vector(1,1,1)
c = cross_product(a, b)
d = dot_product(a, b)
```

4. Matrix-vector multiplication
```python
mat = Matrix([[1,2,3],[-1,0,1],[3,4,5]])
a = mat * Vector(1,2,3)
```


5. Matrix-matrix multiplication
```python
a = Matrix([[1,2,3],[-1,0,1],[3,4,5]])
b = Matrix([[1,5,0],[1,1,1],[12,17,96]])
c = 4.1 * a * b
```

6. Vector rotation
```python
a = Vector(3,4)
b = a.rotated(0.5 * math.pi)
```

7. Matrix transpose
```python
a = Matrix([[1,2,3],[-1,0,1],[3,4,5]])
b = a.transpose()
```

8. Matrix row and column getters
```python
a = Matrix([[1,2,3],[-1,0,1],[3,4,5]])
u = a.get_row(1)
v = a.get_col(0)
```
