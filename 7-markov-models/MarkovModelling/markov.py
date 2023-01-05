import numpy as np
import scipy as sp

class MarkovChain:
    """
    State i will have name States[i].
    P(x_1 = j | x_0 = i) = TransitionMatrix[i,j].
    """
    def __init__(self, TransitionMatrix: np.ndarray, States=None, rng_seed=None):
        # params
        self.P = TransitionMatrix
        if self.P.shape[0] != self.P.shape[1]: raise ValueError("Transition matrix should be square")
        
        self.Pcum = self.P.cumsum(axis=1)
        
        self.n_states = self.P.shape[0]
        self.state_names = States

        self.rng = np.random.default_rng(rng_seed)

        # run
        self.state = np.zeros(self.n_states)
        self.history = []
        
    def setstate(self, i):
        self.state = i
        self.history = [i]

    def setseed(self,seed):
        self.rng = np.random.default_rng(seed)

    def evolve(self, n_steps=1):
        if n_steps == 1:
            p = self.rng.random() # U[0;1]
            j = 0
            for idx,cp in enumerate(self.Pcum[self.state]):
                if p <= cp: j = idx; break
            self.state = j
            self.history.append(j)
        else: 
            for i in range(n_steps):
                self.evolve()

