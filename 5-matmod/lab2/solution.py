import numpy as np
from simplex2 import Simplex
from scipy.optimize import linprog

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
        [-2, -3],
        [0, -4],
        [1, -2],
        [-1, 4],
        [-3, -8],
        # [1, 0],
        # [0, 1]
    ])
    b = np.array([
        10,11,7,11,6,
        # 0, 0
    ])
    c = np.array([6,3])
    # return linprog(c=c, A_ub=A, b_ub=-b, method='simplex')

    return Simplex(debug=True).minimize(-c, None, None, A, -b)

def ex3():
    A = np.array([
        [-17,-13,-11],
        [-5,-5,-10],
        [-6,-3,-9]
    ])
    b = np.array([
        500,400,320
    ])
    c = np.array([-12,-11,-7])
    # return linprog(c=c, A_ub=-A, b_ub=b, method='simplex')

    return Simplex(debug=True).minimize(c, None, None, A, -b)

def ex4():
    A = np.array([
        [2,0,-1,1,3],
        [3,4,2,-4,8],
    ])
    b = np.array([
        [6,3]        
    ])
    c = np.array([10,11,7,11,6])
    # return linprog(c=c, A_ub=-A, b_ub=b, method='simplex')

    return Simplex(debug=True).minimize(c, None, None, A, b)

def ex5():
    A = np.array([
        [6,5],
        [11,7]
    ])
    b = np.array([
        80, 70
    ])
    c = np.array([5,10])
    # return linprog(c=c, A_ub=-A, b_ub=b, method='simplex')

    return Simplex(debug=True).minimize(c, None, None, A, b)

def ex5_1():
    A = -np.array([
        [6,5],
        [11,7]
    ]).T
    c = -np.array([
        80, 70
    ])
    b = -np.array([5,10])
    # return linprog(c=c, A_ub=-A, b_ub=b, method='simplex')

    return Simplex(debug=True).minimize(c, None, None, A, b)

def dz_1():
    problems = [
        {
            'A_eq': np.array([
                [4,1,1,1],
                [9,7,3,2]
            ]),
            'b_eq': np.array([49,134]),
            'c': -np.array([-5,23,2,-3])
        },
        {
            'A_eq': np.array([
                [1,6,-1,-1,0],
                [-1,5,0,-1,0],
                [2,7,0,-1,1]
            ]),
            'b_eq': np.array([10,1,37]),
            'c': np.array([-2,3,4,-2,-2])
        }
        # {
        #     'A_eq': np.array([
        #         [5,-1,2,-1,0,0],
        #         [2,5,-1,-1,0,0],
        #         [5,-4,0,0,2,-1]
        #     ]),
        #     'b_eq': np.array([10,4,-9,10]),
        #     'c': np.array([4,-14,4,-1,2,-3])
        # },
    ]
    solutions = [
        np.array([11,5,0,0]),
        np.array([0,18,9,89,0])
        # np.array([5,1,0,11,0,11]),
    ]

    for args, sol in zip(problems,solutions):
        ans = Simplex(debug=True).minimize(**args)
        if not (ans is None):
            print("="*20)
            print("Solution:")
            # print(sol)
            print("x:", ans['x'])
            print("val:", ans['val'])
            
            if np.linalg.norm(ans['x']-sol) < 1e-8:
                print(">>> RIGHT <<<")

def dz_2():
    problems = [
        {
            'A_eq': np.array([
                [4,1,1,1],
                [9,7,3,2]
            ]),
            'b_eq': np.array([49,134]),
            'c': -np.array([-5,23,2,-3])
        },
        {
            'A_eq': np.array([
                [1,6,-1,-1,0],
                [-1,5,0,-1,0],
                [2,7,0,-1,1]
            ]),
            'b_eq': np.array([10,1,37]),
            'c': np.array([-2,3,4,-2,-2])
        }
        # {
        #     'A_eq': np.array([
        #         [5,-1,2,-1,0,0],
        #         [2,5,-1,-1,0,0],
        #         [5,-4,0,0,2,-1]
        #     ]),
        #     'b_eq': np.array([10,4,-9,10]),
        #     'c': np.array([4,-14,4,-1,2,-3])
        # },
    ]
    solutions = [
        np.array([11,5,0,0]),
        np.array([0,18,9,89,0])
        # np.array([5,1,0,11,0,11]),
    ]

    for args, sol in zip(problems,solutions):
        ans = Simplex(debug=True).minimize(**args)
        if not (ans is None):
            print("="*20)
            print("Solution:")
            # print(sol)
            print("x:", ans['x'])
            print("val:", ans['val'])
            
            if np.linalg.norm(ans['x']-sol) < 1e-8:
                print(">>> RIGHT <<<")

dz_1()

# print("="*20)
# print("Solution:")
# # print(sol)
# print("x:", sol['x'])
# print("val:", sol['val'])
