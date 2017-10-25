import numpy as np

# init variables
a = np.matrix([[1, 0, 0, 0], [0.2, 0.3, 0.1, 0.4], [0.2, 0.5, 0.2, 0.1], [0.7, 0.1, 0.1, 0.1]]) # Transition proba (i=nb of state j=nb of sample)
b = np.matrix([[1, 0, 0, 0, 0], [0, 0.3, 0.4, 0.1, 0.2], [0, 0.1, 0.1, 0.7, 0.1], [0, 0.5, 0.2, 0.1, 0.2]]) # Emission proba -j=nb of state k=nb of output)
T = 5
N = 4
z_init = 1 # Initial state (Range between 0 and N-1)

x = [1, 3, 2, 0] # outputs of the system



# HMM Forward algorithm
def forward(a, b, x):
    alpha = np.zeros((N, T))

    for t in range(T):
        for j in range(N):
            if t == 0:
                if j == z_init:
                    alpha[j, t] = 1
                else:
                    alpha[j, t] = 0
            else:
                alpha[j, t] = b[j, x[t-1]]*np.sum(np.multiply(a[:, j], alpha[:, t-1]))
    print(alpha)

    probmodel = alpha[0, T-1]
    print("Probamodel forward " + str(probmodel))
    return alpha

# HMM Backward algorithm
def backward(a, b, x):
    beta = np.zeros((N, T))

    probmodel = beta[0, T - 1]
    print("Probamodel backward " + probmodel)
    return beta



forward(a, b, x)