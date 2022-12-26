"""
Copied from hmm_learn.ipynb with following changes:
- Add read_textfile offset
- Removed space(0x20) and '(0x27) from valid characters
"""

import numpy as np
from collections import namedtuple

LETTERS = bytes("іґєїабвгдежзийклмнопрстуфхцчшщьюя", '1251')

def notalpha(c):
    return c < 0xBF and c!=0xA5 and c!= 0xAA and c!=0xAf and c!=0xB2 and c!=0xB3 and c!=0xB4 and c!= 0xBA

def tolower(c):
    # if c < 0 or c > 255: return None
    dict = (0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f, 0x40, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f, 0x90, 0x83, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x9a, 0x8b, 0x9c, 0x9d, 0x9e, 0x9f, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f, 0xa0, 0xa2, 0xa2, 0xbc, 0xa4, 0xb4, 0xa6, 0xa7, 0xb8, 0xa9, 0xba, 0xab, 0xac, 0xad, 0xae, 0xbf, 0xb0, 0xb1, 0xb3, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xbb, 0xbc, 0xbe, 0xbe, 0xbf, 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef, 0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa, 0xfb, 0xfc, 0xfd, 0xfe, 0xff, 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef, 0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa, 0xfb, 0xfc, 0xfd, 0xfe, 0xff)
    return dict[c]

def read_textfile(file, char_limit=1000000, char_offset=0):
    data = bytearray()
    with open(file, 'rb') as f:
        checkpoint = 10000
        n_res_bytes = 0
        n_read_bytes = 0
        counter = 0
        offset_counter = char_offset

        c = 0
        while True:
            n_read_bytes += 1
            d = f.read(1)
            if len(d) == 0:
                c = None
                break
            c = d[0]

            if notalpha(c): 
                # print(f"'{c}' is not alpha")
                continue

            # if we are here, the char is ok
            if offset_counter > 0:
                offset_counter -= 1
                if offset_counter % checkpoint == 0:
                    print(f"offset checkpoint {offset_counter} ({n_read_bytes})")
                continue
            if offset_counter == 0:
                print("Offset done. Starting reading actual data.")
                offset_counter = -1

            c = tolower(c)
            # print(f"tolower {c}")
            data.append(c)
            counter += 1
            n_res_bytes += 1
            if counter == checkpoint:
                counter = 0
                print(f"read checkpoint {n_res_bytes} ({n_read_bytes})")
            if n_res_bytes > char_limit: 
                break
        print("read - end")
    return data

###
###
###


BaumWelch_params = namedtuple('BaumWelch_params', 'max_iter, eps, n_hidden_states, n_observation_states, n_observations, const_Mu, const_A, const_B')
STOCHASTIC_EPS = 1e-8


# X, Y: T
# mu: 1xN
# A: NxN
# B: NxM

# P_lambda(Y0=y0,...,YT=yT) = alpha[T].sum()
def calculate_alpha(Y, estMu, estA, estB, params):
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations
    alpha = np.empty((T, N))
    C = np.empty(T)

    alpha[0] = estMu * estB[:, Y[0]]
    C[0] = 1/alpha[0].sum()
    alpha[0] *= C[0]
    
    for t in range(1, T):
        # alpha[t,k] = sum_i alpha[t-1, i] * A[i, k] * B[k, y[t]]
        try:
            alpha[t] = (alpha[t-1] @ estA) * estB[:, Y[t]]
        except IndexError as err:
            print(err)
            print(f"t {t}")
            raise ValueError("")
        # for k in range(N):
        #     alpha[t, k] = (alpha[t-1] @ estA[:,k]) * estB[k, Y[t]] # todo: optimize
        #     if np.abs(alt[k]-alpha[t,k]) > 1e-5: raise ValueError(f"alpha different at {t},{k}")
        C[t] = 1/alpha[t].sum()
        alpha[t] *= C[t]
    
    if alpha.shape != (T, N): raise ValueError("ShapeMismatch")
    return alpha, C

# P_lambda(Y0=y0,...,YT=yT) = Mu * beta[0] @ B
def calculate_beta(C, Y, estMu, estA, estB, params):
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations
    beta = np.empty((T, N))

    beta[T-1, :] = C[T-1]

    for t in range(T-2, -1, -1):
        # beta[t,k] = sum_i  beta[t+1, i] * A[k,i] * B[i, Y[t+1]] * c
        beta[t] = (estA * estB[:, Y[t+1]] * beta[t+1]).sum(axis=1) * C[t]
        # for k in range(N):
        #     beta[t,k] = (estA[k] * estB[:, Y[t+1]] * beta[t+1]).sum() * C[t] # todo: optimise
        #     if np.abs(alt[k]-beta[t,k]) > 1e-6: raise ValueError(f"beta different at {t},{k}")

    if beta.shape != (T, N): raise ValueError("ShapeMismatch")
    return beta

def calculate_gamma(alpha, beta, params):
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations
    gamma = np.empty((T, N))
    gamma = alpha * beta
    gamma = gamma / gamma.sum(axis=1, keepdims=True)
    
    if (np.abs(gamma.sum(axis=1) - 1) > STOCHASTIC_EPS).any(): raise ValueError(f"gamma is not stochastic! s={gamma.sum(axis=1)}")
    if gamma.shape != (T, N): raise ValueError("ShapeMismatch")
    return gamma

def calculate_gamma_alt(xi, params):
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations
    gamma = np.empty((T, N))
    gamma = xi.sum(axis=2)
    
    # if (np.abs(gamma.sum(axis=1) - 1) > STOCHASTIC_EPS).any(): raise ValueError(f"gamma is not stochastic! s={gamma.sum(axis=1)}")
    if gamma.shape != (T, N): raise ValueError("ShapeMismatch")
    return gamma

def calculate_xi(alpha, beta, Y, estMu, estA, estB, params):
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations
    xi = np.empty((T, N, N))
    for t in range(0, T-1):
        xi[t] = alpha[t].reshape(-1,1) * estA * estB[:, Y[t+1]] * beta[t+1]
        # xi[t] /= xi[t].sum()
        # if (np.abs(xi[t].sum() - 1) > STOCHASTIC_EPS): raise ValueError(f"xi[{t}] is not stochastic! s={xi[t].sum()}")
    # print("xi sum mean: ", xi.sum(axis=1).mean())
    
    if xi.shape != (T, N, N): raise ValueError("ShapeMismatch")
    return xi

def reestimate(alpha, beta, gamma, xi, Y, params):
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations

    estMu = None
    if not params.const_Mu:
        estMu = gamma[0]
    estA = None
    if not params.const_A:
        estA = xi.sum(axis=0) / gamma[:-1].sum(axis=0).reshape(-1,1)
    
    estB = None
    if not params.const_B:
        estB = np.zeros((N,M))

        for t in range(0, T):
            estB[:,Y[t]] += gamma[t]
        estB = estB / gamma.sum(axis=0).reshape(-1,1)

    return estMu, estA, estB

def evaluate(C):
    # мінус _потрібен_!
    return -np.log(C).sum()

def learn_iterate(Y, Mu, A, B, params, alpha=None, c=None):
    if (alpha is None or c is None):
        alpha, c = calculate_alpha(Y, Mu, A, B, params)
    beta = calculate_beta(c, Y, Mu, A, B, params)
    xi = calculate_xi(alpha, beta, Y, Mu, A, B, params)
    gamma = calculate_gamma(alpha, beta, params)
    # gamma = calculate_gamma_alt(xi, params) 
    return reestimate(alpha, beta, gamma, xi, Y, params)


BaumWelch_init = namedtuple('BaumWelch_init', 'Mu, A, B')
BaumWelch_result = namedtuple('BaumWelch_result', 'Mu, A, B, prob, iters')

# X, Y: T
# mu: 1xN
# A: NxN
# B: NxM
def learn(Y:list[int], params:BaumWelch_params, init_vals=(None, None, None), seed=42):
    np.random.seed(seed)
    N, M, T = params.n_hidden_states, params.n_observation_states, params.n_observations
    
    Mu, A, B = init_vals
    if Mu is None: 
        Mu = np.ones(N) + (np.random.rand(N) - 0.5)*0.001
        Mu = Mu / Mu.sum()
    if A is None: 
        A = np.ones((N,N)) + (np.random.rand(N,N) - 0.5)*0.001
        A = A / A.sum(axis=1, keepdims=True)
    if B is None: 
        B = np.ones((N,M)) + (np.random.rand(N,M) - 0.5)*0.001
        B = B / B.sum(axis=1, keepdims=True)

    if (np.abs(Mu.sum() - 1) > STOCHASTIC_EPS).any(): raise ValueError(f"Initial Mu is not stochastic! s={Mu.sum()}")
    if (np.abs(A.sum(axis=1) - 1) > STOCHASTIC_EPS).any(): raise ValueError(f"Initial A is not stochastic! s={A.sum(axis=1)}")
    if (np.abs(B.sum(axis=1) - 1) > STOCHASTIC_EPS).any(): raise ValueError(f"Initial B is not stochastic! s={B.sum(axis=1)}")


    alpha, c = calculate_alpha(Y, Mu, A, B, params)
    print("init c:", c)
    prob = evaluate(c)
    print(f"Starting Baum-Welch process. Initial probability = {prob}")
    print("Initial Mu:", Mu)
    print("Initial A:", A)
    print("Initial B:", B)
    counter = 0
    while True:
        counter += 1
        newMu, newA, newB = learn_iterate(Y, Mu, A, B, params, alpha, c)

        if newMu is not None and (np.abs(newMu.sum() - 1) > STOCHASTIC_EPS).any(): 
            raise ValueError(f"New Mu is not stochastic! iter = {counter}, s={newMu.sum()}")
        if newA is not None and (np.abs(newA.sum(axis=1) - 1) > STOCHASTIC_EPS).any(): 
            raise ValueError(f"New A is not stochastic! iter = {counter}, s={newA.sum(axis=1)}")
        if newB is not None and (np.abs(newB.sum(axis=1) - 1) > STOCHASTIC_EPS).any(): 
            raise ValueError(f"New B is not stochastic! iter = {counter}, s={newB.sum(axis=1)}")

        if params.const_Mu: newMu = Mu
        if params.const_A: newA = A
        if params.const_B: newB = B

        alpha, c = calculate_alpha(Y, newMu, newA, newB, params)
        new_prob = evaluate(c)

        if new_prob - prob < params.eps:
            # intentionally no abs to handle new_prob < prob 
            print("Stopping on eps")
            break
        Mu, A, B = newMu, newA, newB
        prob = new_prob

        if counter > params.max_iter:
            print("Stopping on max_iter")
            break
        print(f"Iteration {counter} finished. p={prob}")

    return BaumWelch_result(Mu, A, B, prob, counter)



def text2states(data, N):
    Y = []
    for i,c in enumerate(data):
        if i >= N: break
        y = LETTERS.find(c)
        if y < 0:
            print(f"ERROR: invalid character {c} (somehow) at index {i}")
            break
        Y.append(y)
    return np.array(Y, np.uint8)

def score(a, b):
    return (a == b).mean()
