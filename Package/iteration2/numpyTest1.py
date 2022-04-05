import numpy as np
from numpy.linalg import inv

a = np.array([np.zeros(2)])
b = np.zeros((1,2))
d = np.array([[1., 2.]])
c = d.T
e = np.zeros((4,1))
h = np.zeros((5,5))
g = np.zeros(5)
"""
print(a.T)
print(d)
print(c)
print(h)
"""
print(g)

#indexing
print(e[1,0])
print(e[1][0])


#Z method
x = np.array([1., 2., 3., 4., 5.])
y = np.array([10, 8, 7.7, 6.2, 6])
print("\n", sum(x))

n = len(x)
A = np.zeros((n,n))
b = np.zeros((n, 1))

for row in range(n):
    for col in range(n):
        if row == 0 and col == 0:
            A[0][0] = n
        else:
            #print(col+row)
            A[row,col] = sum(np.power(x, col+row))
    print(row)

    b[row, 0] = sum(np.multiply(y, np.power(x, row)))
print(A)
print(b)
print()

print(x)
print(type(x))
print(inv(A))
coef = np.matmul(inv(A), b)
print(coef)

