import numpy as np
from simplex2 import Simplex

# A = np.array([
#     [1, 1],
#     [3, -1],
#     [0, -1],
#     [-3, -2],
#     [-1, 3]
# ])
# b = np.array([
#     3, 5, -4, -26, -5
# ])
# c = np.array([-1,3])

# sol = Simplex().minimize(c, A_ge=A, b_ge=b, debug=True);
# print()
# print(sol['xs'])
# print(sol['val'])
# print(sol['table_xs'])
# print(sol['table'])

def ex2_4_d():
    A = np.array([
        [3, 2],
        [6, 1],
        [0, 1]
    ])
    b = np.array([
        6,6,1
    ])
    c = np.array([15,33])
    # linprog(c=c, A_ub=-A, b_ub=-b, method='simplex')

    return Simplex(debug=True).minimize(c, None, None, A, b)

sol = ex2_4_d()

print("="*20)
print("Solution:")
if 'xs' in sol:
    print("xs:", sol['xs'])
    print("table_xs:", sol['table_xs'])
else:
    print("x:", sol['x'])
print("val:", sol['val'])
