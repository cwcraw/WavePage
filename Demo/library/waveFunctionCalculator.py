import numpy as np
from Demo.library.potentialEnum import PotentialEnum


def WaveCalc(pot):
    # Defining basic parameters for the potential of the wave function
    m = 200
    x = range(m)
    V = [0] * m
    if pot == PotentialEnum.MORSE:
        # Morse potential
        for n in range(0, m):
            V[n] = 0.01 * (1 - (2.718) ** (-0.1 * (n / 4 - 10))) ** 2
    elif pot == PotentialEnum.BARRIER:
        # rectangular barrier
        for n in range(80, 120):
            V[n] = 0.1
    elif pot == PotentialEnum.HIGH_BARRIER:
        # rectangular barrier high energy
        for n in range(80, 120):
            V[n] = 0.5
    elif pot == PotentialEnum.STEP:
        # Change in pot
        for n in range(100, 200):
            V[n] = 0.01
    elif pot == PotentialEnum.HO:
        # Harmonic Oscilator
        for n in range(0, m):
            V[n] = 0.00001 * (n - m / 2 + 0.5) ** 2
    # The next two are a bit redundant and probably can be refactored
    elif pot == PotentialEnum.OPEN:
        for n in range(0, m):
            V[n] = 0
    else:
        for n in range(0, m):
            V[n] = 0

    tmp_arr = []
    output_mat = []
    # Creating the Hamiltonian operator, a matrix.
    # The Hamiltonian is 2nd derivative of the wavefunction (times a constant) plus the potential.
    # Here I'm using a finite difference method to form the Hamiltonian.
    # The first two cases are the first and final row of the matrix, while the third case is the body of the matrix
    for n in range(0, m):
        tmp_arr = [0] * m
        if n == 0:
            tmp_arr[0] = 2 + V[0]
            tmp_arr[1] = -1
        elif n == m - 1:
            tmp_arr[m - 2] = -1
            tmp_arr[m - 1] = 2 + V[m - 1]
        else:
            tmp_arr[n - 1] = -1
            tmp_arr[n] = 2 + V[n]
            tmp_arr[n + 1] = -1
        output_mat.append(tmp_arr)
    # Here numpy makes our life easy by finding the eigenvalues and vectors. We will display the eigenvectors in our gui
    E_val_1, E_vec_1 = np.linalg.eig(output_mat)
    # Here numpy makes our life difficult by return the eigenvalues & vectors unsorted.
    # I use a simple bubble sort to sort the values and vectors together. I would like to refactor this to make it more efficient.
    for i in range(1, len(E_val_1) - 2):
        for j in range(0, len(E_val_1) - i):
            if E_val_1[j] > E_val_1[j + 1]:
                E_val_1[j], E_val_1[j + 1] = E_val_1[j + 1], E_val_1[j]
                for k in range(0, len(E_val_1)):
                    E_vec_1[k, j], E_vec_1[k, j + 1] = E_vec_1[k, j + 1], E_vec_1[k, j]

    return E_val_1, E_vec_1, V, x
