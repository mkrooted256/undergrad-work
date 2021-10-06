import numpy as np
import itertools as it

# Algorithm

def show_table(A, col_labels, row_labels, selected=[]):
    width = max(map(len, col_labels + row_labels)) + 2

    if width < 7: width = 7

    s = ""
    s += ' '*width
    s += '|'
    for x in col_labels:
        s += x.ljust(width) + '|'
    s += '\n'
    s += ('-'*width + '+')*(len(col_labels) + 1) + '\n'

    for i, ylabel in zip(range(A.shape[0]), row_labels):
        s += ylabel.ljust(width) + '|'
        for j in range(A.shape[1]):
            # print((i,j), selected)
            if (i,j) not in selected:
                s += (f"{A[i,j]:.2f}"+' ').rjust(width) + '|'
            else:
                s += (f"[{A[i,j]:.2f}]").rjust(width) + '|'
        s += '\n'

    return s

def det(A, i_base, j_base, i, j):
    return A[i_base, j_base] * A[i,j] - A[i_base,j]*A[i,j_base]

def jordan_swap(A, i, j):
    n,m = A.shape
    a = A[i,j]
    B = np.zeros_like(A) # new matrix full of zeros
    B[i, :] = -A[i, :] # copy base row * -1
    B[:, j] =  A[:, j] # copy base column
    B[i,j] = 1 # set base element to 1

    for p in it.chain(range(0,i), range(i+1,n)):
        for q in it.chain(range(0,j), range(j+1,m)):
            B[p,q] = det(A, i, j, p, q)
    return B / a

def eliminate(A, j):
    _,m = A.shape
    idx = list(it.chain(range(0, j), range(j+1, m)))
    return A[:, idx]

def remove_negative_b(A):
    # Знаходимо мiнiмальне з вiдношень 
    # вiд’ємних вiльних членiв до додатнiх елементiв у їх рядках

    m,n = A.shape
    b = A[0:m-1, -1] # save last column + exclude last row
    
    id = -1
    min = np.Inf
    for i in range(m-1):
        for j in range(n-1):
            if A[i,j] > 0 and b[i] < 0 and b[i] / A[i,j] < min:
                id = i,j

    return id

def remove_negative_c(A):
    # Знайти всi вiдношення (додатнiх) вiльних членiв до вiд’ємних елементiв 
    # у їх рядках, якi належать стовпчикам з вiд’ємними оцiнками.
    # Вiд’ємний елемент, який дає найбiльше вiдношення (найменше 
    # за абсолютною величиною) обрати за ведучий i виконати крок 
    # жорданових перетворень.
    
    m,n = A.shape
    b = A[0:m-1, -1] # save last column + exclude last row
    c = A[-1, 0:n-1]

    id = -1
    max = -np.Inf
    for i in range(m-1):
        for j in range(n-1):
            if c[j]<0 and A[i,j] < 0 and b[i] > 0 and b[i] / A[i,j] > max:
                id = i,j
    if (id == -1):
        print(A)
    return id

def is_optimizable(A):
    # Якщо в процесi пошуку оптимального плану у деякому стовпчику з 
    # вiд’ємною оцiнкою вiдсутнi вiд’ємнi елементи, то задача не має 
    # оптимального розв’язку, тобто цiльова функцiя необмежена.
    m,n = A.shape
    c = A[-1, 0:n-1]
    c_negatives = np.nonzero(c < 0)[0]
    # print(c_negatives)
    a_negatives = A[0:m-1, c_negatives] < 0
    # print(a_negatives)

    # system is ok if ALL (c<0)-columns have 
    # at least one (ANY) element negative
    return all(np.any(a_negatives, axis=0))

def is_feasible(A):
    # Розв'язок допустимий якщо всі вільні члени 
    # (останній стовпчик) невід'ємні
    return all(A[:,-1] >= 0)

def is_consistent(A):
    # Якщо у деякому рядку з вiд’ємним вiльним членом немає додатнiх
    # елементiв, то змiнити знак вiльного члена неможливо, що 
    # свiдчить про вiдсутнiсть допустимого розв’язку
    m,n = A.shape
    b = A[0:m-1, -1] # save last column + exclude last row
    b_negatives = np.nonzero(b < 0)[0]
    a_positives = A[b_negatives, 0:n-1] > 0

    # system is ok if ALL (b<0)-rows have 
    # at least one (ANY) element positive
    return all(np.any(a_positives, axis=1))

def is_optimal(A):
    # Ознакою оптимальностi плану є невiд’ємнiсть оцiнок (c_i)
    return all(A[-1, 0:A.shape[1]-1] > 0)

def uni_simplex(A, xlabels=None, ylabels=None):
    m,n = A.shape
    b = A[0:m-1, -1]
    c = A[-1, 0:n-1]
    nonbasis = list(range(0,n-1)) # b is n-1
    basis = list(range(n-1,n+m-2)) # F is n+m-2

    xlabels = xlabels or (['x'+str(i) for i in range(1,n)] + ['b'])
    ylabels = ylabels or (['y'+str(i) for i in range(1,m)] + ['F'])

    error = None

    def swap(i, j):
        nonlocal A, xlabels, ylabels, basis, nonbasis
        print(show_table(A, xlabels, ylabels, [(i, j)]))
        A = jordan_swap(A, i, j)
        # print(i,j)
        # print(xlabels, ylabels, basis, nonbasis)
        # swap labels
        xlabels[j], ylabels[i] = ylabels[i], xlabels[j]  
        # swap indices 
        nonbasis[j], basis[i] = basis[i], nonbasis[j] 

    while not is_feasible(A):
        if not is_consistent(A):
            error = 'inconsistent'
            print(show_table(A, xlabels, ylabels))
            print(error)
            return error
        i, j = remove_negative_b(A)  
        swap(i, j)

    print("Feasible solution found. No b<0:")
    print(show_table(A, xlabels, ylabels))
    print("Start finding optimal solution...")

    while not is_optimal(A):
        if not is_optimizable(A):
            error = 'inoptimizable'
            print(show_table(A, xlabels, ylabels))
            print(error)
            return error
        i, j = remove_negative_c(A)
        swap(i, j) 

    print("Optimal solution found. No c<0:")
    print(show_table(A, xlabels, ylabels))

    x = A[0:n-1, -1]
    F = A[-1,-1]

    print("\nOptimal x = ",x,"; with F(x) = ",F)
    return x, F
    

# --------------------------------------------------- #

# A = np.array([
#     [ 1, 0,  0, -1,  0, -2, -5],
#     [ 0, 1,  0,  2, -3,  1, -3],
#     [ 0, 0,  1,  2, -5,  6, -5],
#     [ 1, 1,  1,  0,  0,  0,  0]
# ])
# labels_r = ['y1','y2','y3','F']
# labels_c = ['x1','x2','x3','x4','x5','x6','b']

# uni_simplex(A, labels_c, labels_r)
