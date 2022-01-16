import numpy as np
import itertools as it


def show_table(A, col_labels, row_labels, selected=[]):
    A = np.matrix(A)
    
    width = max(map(len, col_labels + row_labels)) + 2

    if width < 7: width = 11

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
                s += (f"{A[i,j]:.5f}"+' ').rjust(width) + '|'
            else:
                s += (f"[{A[i,j]:.5f}]").rjust(width) + '|'
        s += '\n'

    return s

class Simplex:
    def __init__(self, eps=1e-12, debug=True):
        self.debug = debug
        self.eps = eps
        self.A = None
        # self.b = None
        self.c = None
        self.basis_labels = None
        self.nonbasis_labels = None

    def jordan_swap(self, i, j):
        n,m = self.A.shape
        a = self.A[i,j]
        B = np.zeros_like(self.A) # new matrix full of zeros
        B[i, :] = -self.A[i, :] # copy base row * -1
        B[:, j] =  self.A[:, j] # copy base column
        B[i,j] = 1 # set base element to 1

        self.basis_labels[i], self.nonbasis_labels[j] = \
            self.nonbasis_labels[j], self.basis_labels[i]

        for p in it.chain(range(0,i), range(i+1,n)):
            for q in it.chain(range(0,j), range(j+1,m)):
                det = self.A[i,j] * self.A[p,q] - self.A[i,q] * self.A[p,j]
                B[p,q] = det
        self.A = B / a
        return self.A

    def eliminate_col(self, j):
        ids = list(range(j)) + list(range(j+1, self.A.shape[1]))
        self.A = self.A[:, ids]
        del self.nonbasis_labels[j]
        return self.A
        
    def print(self, i=None, j=None):
        if not self.debug: return
        if not i is None:
            print(show_table(self.A, self.nonbasis_labels, self.basis_labels, [(i,j)]))
        else:
            print(show_table(self.A, self.nonbasis_labels, self.basis_labels))

    def get_c(self):
        return self.A[-1, 0:self.A.shape[1]-1]
    def get_b(self):
        return self.A[0:self.A.shape[0]-1, -1]

    def is_optimal(self):
        return all(self.get_c() >= -self.eps)

    def is_feasible(self):
        return all(self.get_b() >= self.eps)

    def find_feasible(self):
        # (x - nonbasis vars, y - basis vars)
        # All x = 0
        # y_i = (Ax)_i + b_i = b_i
        # We are tweaking x_j. What y_i goes to 0 first?
        # y_i = A_ij x_j + b_i >= 0 (no sums! j is const!)
        # =>   x_j >= - b_i / A_ij

        k, min = None, np.Inf
        b = self.get_b()
        if(self.debug): print("feasibles: ", end='')
        for i in range(self.A.shape[0]-1):
            for j in range(self.A.shape[1]-1):
                a = self.A[i,j]
                if a > self.eps and b[i] < -self.eps and b[i] / a < min:
                    k = i,j
                    min = b[i] / a
                    if self.debug: print("(", k, min, ") ", end='')
        if self.debug: print()
        return k

    def find_optimal(self):
        k, max = None, -np.Inf
        b = self.get_b()
        c = self.get_c()
        if(self.debug): print("optimals: ", end='')
        for i in range(self.A.shape[0]-1):
            for j in range(self.A.shape[1]-1):
                a = self.A[i,j]
                if a < -self.eps and c[j] < -self.eps and  b[i] / a > max:
                    k = i,j
                    max = b[i] / a
                    if self.debug: print("(", k, max, ") ", end='')
        # if k is not None: print("a:",self.A[k[0],k[1]])
        if self.debug: print()
        return k

    def extract_x(self):
        x = np.zeros(len(self.xlabels))
        b = self.get_b()
        # print(self.xlabels)
        for i_x, L in enumerate(self.xlabels):
            for j, q in enumerate(self.basis_labels):
                if q == L:
                    # print(i_x, L, j, q)
                    x[i_x] = b[j]
                    break
            # else x_i is 0
        return x

    def extract_xs(self):
        # infinite solutions
        c0 = (-self.eps < self.A[-1,:]) & (self.A[-1,:] < self.eps)
        c0[-1] = True
        rows = []
        rows_l = []
        cols_l = []
        for i_x, L in enumerate(self.xlabels):
            for j, q in enumerate(self.basis_labels):
                if q == L:
                    # print(i_x, L, j, q)
                    rows.append(i_x)
                    rows_l.append(L)
                    break
        for j, q in enumerate(self.nonbasis_labels):
            if c0[j]:
                # print(i_x, L, j, q)
                cols_l.append(L)
                break
        cols_l.append('1')
        
        return self.A[rows,c0], rows_l, cols_l
        

    def minimize(self, c, A_eq=None, b_eq=None, A_ge=None, b_ge=None, eliminate_only=False, debug=None):
        if debug is not None: self.debug = debug
        
        self.xs = list(range(c.reshape(1,-1).shape[0]))

        m_ge, n = 0, 0
        m_eq, _ = 0, 0
        self.basis_labels = []

        wtf = True

        if not A_ge is None:
            wtf = False
            m_ge, n = A_ge.shape
            self.basis_labels += [f'y{i+1}' for i in range(m_ge)]

        if not A_eq is None:
            wtf = False
            m_eq, n = A_eq.shape
            self.basis_labels += [f'eq{i+1}' for i in range(m_eq)]
    
        if wtf:
            print("wtf")
            return

        self.nonbasis_labels = [f'x{i+1}' for i in range(n)] 
        self.xlabels = self.nonbasis_labels.copy()
        self.nonbasis_labels += ['1']
        self.basis_labels += ['C']


        m = m_ge + m_eq
        if not A_ge is None:
            self.A = np.append(A_ge, -b_ge.reshape(-1,1), axis=1)


        # Prepare Aug if there are equalities
        if not A_eq is None:
            # create and eliminate columns with y_i = 0
            if A_ge is None:
                A = A_eq
                b = b_eq
            else:
                A = np.vstack([A_ge, A_eq])
                b = np.vstack([b_ge, b_eq])
            self.A = np.append(A, -b.reshape(-1,1), axis=1)

            self.A = np.vstack([self.A, np.zeros(n+1)])
            self.A[-1,0:n] = c
            self.c = c

            # js = []
            for i in range(m_ge, m_ge + m_eq):
                for j in range(n):
                    # find first nonzero element
                    if np.abs(self.A[i, j]) > self.eps:
                        # and choose it as the base
                        self.print(i, j)
                        self.jordan_swap(i, j)
                        # self.print()
                        self.eliminate_col(j)
                        n -= 1
                        break 
            self.c = self.A[-1, 0:self.A.shape[1]-1]
        self.print()
        if debug: print("Equalities eliminated.\n")
        if eliminate_only: return

        if A_eq is None:
            self.A = np.append(A_ge, -b_ge.reshape(-1,1), axis=1)
            self.A = np.vstack([self.A, np.zeros(n+1)])
            self.A[-1,0:n] = c
            self.c = c

        # Find feasible region
        while not self.is_feasible():
            id = self.find_feasible()
            if id is None:
                print("Error: inconsistent")
                self.print()
                return
            self.print(*id)
            if self.debug: 
                print("=> x: ", self.extract_x())
                print("-"*20)
                print()
            self.jordan_swap(*id)
        
        if debug: print("Feasible solution found. Finding optimum...\n")
        
        # Optimize
        while not self.is_optimal():
            # find entering basis variable.
            # It will be the one with the largest absolute val of C.
            # That is, the one which minimize F the steepest
            id = self.find_optimal()
            if id is None:
                print("Error: inoptimizable")
                self.print()
                return

            leave_basis, enter_basis = id
            self.print(leave_basis, enter_basis)
            if self.debug: 
                print("=> x: ", self.extract_x())
                print("-"*20)
                print()
            self.jordan_swap(leave_basis, enter_basis)

        if debug: print("Optimum found!")
        self.print()

        c0 = (-self.eps < self.get_c()) & (self.get_c() < self.eps)
        if any(c0):
            # infinite solutions
            xs, rows_l, cols_l = self.extract_xs()
            return {
                'xs':  xs,
                'val': self.A[-1,-1], 
                'table_xs': show_table(xs, cols_l, rows_l),
                'table': show_table(self.A, self.nonbasis_labels, self.basis_labels)
            }

        return {
            'x': self.extract_x(), 
            'val': self.A[-1,-1], 
            'table': show_table(self.A, self.nonbasis_labels, self.basis_labels)
        }


# -------------


# A_eq = np.array([
#     [ 1, 0,  0, -1,  0, -2],
#     [ 0, 1,  0,  2, -3,  1],
#     [ 0, 0,  1,  2, -5,  6],
# ])
# b_eq = np.array([5, 3, 5])
# c = np.array([1, 1, 1, 0, 0, 0])

# A_eq = np.array([
#     [ 5, -4,  2, -1,  0, 0],
#     [ 2,5,-1,-1,0,0],
#     [ 1,-3,0,0,1,-1],
#     [ 5,-4,0,0,2,-1],
# ])
# b_eq = np.array([10,4,-9,10])
# c = np.array([4,-14,4,-1,2,-3])

# A_ge = np.array([
#     [ 1, 3],
#     [ -1,2],
#     [ 4,1],
# ])
# b_ge = np.array([1,-3,2])
# c = np.array([0,-1])

# A_ge = np.array([
#     [3,-1,4],
#     [1,2,-1],
#     [5,3,2],
# ])
# b_ge = np.array([6,3,8])
# c = np.array([0,0,0])


# Simplex().minimize(c, A_ge=A_ge, b_ge=b_ge)

