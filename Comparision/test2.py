def getValue(a):
    return a + 1

def findValue(a):
    b = a*2
    return getValue(b)

x = findValue(7)
print(x)

b = [1]
print(b*7)

import numpy as np

print([np.nan]*7)