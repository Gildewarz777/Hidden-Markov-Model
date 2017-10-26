import numpy as np
import math

# init variables
a = np.matrix([[1, 0, 0, 0], [0.2, 0.3, 0.1, 0.4],
               [0.2, 0.5, 0.2, 0.1], [0.7, 0.1, 0.1, 0.1]]) # Transition proba (i=nb of state j=nb of sample)
b = np.matrix([[1, 0, 0, 0, 0], [0, 0.3, 0.4, 0.1, 0.2],
               [0, 0.1, 0.1, 0.7, 0.1], [0, 0.5, 0.2, 0.1, 0.2]]) # Emission proba -j=nb of state k=nb of output)
T = 5
N = 4
z_init = 1 # Initial state (Range between 0 and N-1)

x = [1, 3, 2, 0] # outputs of the system



# HMM Forward algorithm
def forward(a, b, x):
    print("Forward")
    alpha = np.zeros((N, T))

    for t in range(T):
        for j in range(N):
            if t == 0:
                if j == z_init:
                    alpha[j, t] = 1
                else:
                    alpha[j, t] = 0
            else:
                sum = 0
                for i in range(N):
                    alpha[j, t] += a[i, j] * alpha[i, t-1]
                print(alpha[i, t-1])
                alpha[j, t] *= b[j, x[t - 1]]
                #alpha[j, t] = b[j, x[t-1]]*np.sum(np.multiply(a[:, j], alpha[:, t-1]))
    print("alpha =")
    print(alpha)

    probmodel = alpha[0, T - 1]
    print("Probamodel forward " + str(probmodel))
    return alpha

# HMM Backward algorithm
def backward(a, b, x):
    print("Backward")
    beta = np.zeros((N, T))
    beta[0, T - 1] = 1

    for t in range(T-2, -1, -1):
        for i in range(N):
        #    if t == T - 1:

         #       if i == 0:
          #          beta[i, t] = 1
           #     else:
            #        beta[i, t] = 0
        #    else:

            for j in range(N):
                beta[i, t] += beta[j, t + 1] * a[i, j] * b[j, x[t]]

    probmodel = beta[N - 1, 0]
    print(beta)
    print("Probamodel backward " + str(probmodel))
    return beta

def estimate_gamma(alpha, beta, a, b, x):
    print("Estimate gamma")
    gamma = np.zeros((N, N, T))
    for t in range(1, T):
        for i in range(N):
            for j in range(N):
                gamma[i, j, t] = alpha[i, t - 1] * a[i, j] * b[j, x[t - 1]] * beta[j, t]


   # print("gamma=")
    #print(gamma)
    return gamma

def update_a(a, gamma, x):
    print("Update a")
    for i in range(N):
        for j in range(N):
            den = 0
            nom = 0
            for t in range(T):
                nom += gamma[i, j, t]
                #print("gamma " + str(gamma[i, j, t]))

                for l in range(N):
                    den += gamma[i, l, t]

            if den == 0:
                den += 1

            #print("nom" + str(nom))
            #print("den" + str(den))

            a[i, j] = nom / den
    a[0, 0] = 1
    return a

def update_b(b, gamma, x):
    print("Update b")

    for j in range(N):
        for k in range(T-1):
            den = 0
            nom = 0

            for t in range(1, T):
                if x[t - 1] == k:
                    b[j, k + 1] += np.sum(gamma[j, :, t])
                    #if t == 3 and k == 2:
                        #print("allo")
                        #print(np.sum(gamma[j, :, t]))
            #print(b[j, k + 1])
            for t in range(1, T):
                den += np.sum(gamma[j, :, t])
                if den == 0:
                    den += 1
            b[j, k + 1] = b[j, k + 1] / den
    b[0, 0] = 1
    return b

def baum_welch(x):
    print("Baum Welch")
    a = np.matrix([[1, 0, 0, 0], [0.2, 0.3, 0.1, 0.4], [0.2, 0.5, 0.2, 0.1],
                   [0.7, 0.1, 0.1, 0.1]])  # Transition proba (i=nb of state j=nb of sample)
    b = np.matrix([[1, 0, 0, 0, 0], [0, 0.3, 0.4, 0.1, 0.2], [0, 0.1, 0.1, 0.7, 0.1],
                   [0, 0.5, 0.2, 0.1, 0.2]])  # Emission proba -j=nb of state k=nb of output)

    print(a)
    print(b)
    iter = 0

    while iter in range(10):
        print("Iteration: " + str(iter))


        # Estimate alpha and beta
        alpha = forward(a, b, x)
        beta = backward(a, b, x)

        # Estimate gamma
        gamma = estimate_gamma(alpha, beta, a, b, x)

        # Update a and beta
        a = update_a(a, gamma, x)
        b = update_b(b, gamma, x)

        print("a=")
        print(a)
        print("b=")
        print(b)

        iter += 1
    return a, b

baum_welch(x)

