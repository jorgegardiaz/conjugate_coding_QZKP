from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import sys
import pandas as pd

#----------------------------------------
# Auxiliary functions
#----------------------------------------
def quantum_random_binary_string(length):
    '''
    Random key generator using quantum randomness.
    '''
    string = []
    for bit in range(length):
        qcoin = QuantumCircuit(1,1)
        qcoin.h(0)
        qcoin.measure(0,0)
        exec = sim.run(qcoin, shots=1).result()
        string.append(int(list(exec.get_counts(qcoin).keys())[0]))
    return string


def psi_gen(w, basis):
    '''
    Generation of the quantum state |psi>.
    '''
    if len(w) != len(basis):
        raise ValueError('Same number of basis and bits expected.')
    psi = []
    for i in range(len(w)):
        qubit = QuantumCircuit(1, 1)
        if w[i] == 1:
            qubit.x(0)
            if np.random.choice([0, 1], p=[1 - pbit, pbit]):
                qubit.x(0)
            if np.random.choice([0, 1], p=[1 - pphase, pphase]):
                qubit.z(0)
        if basis[i] == 1:
            qubit.h(0)
        psi.append(qubit)
    return psi

def challenge_gen(psi, c, b):
    '''
    Generation of the challenge for |psi>.
    '''
    if len(psi) != len(c):
        raise ValueError('Same number of qubits and bits expected.')
    for i in range(len(psi)):
        if c[i] == 1:
            if b[i]==0:
                psi[i].x(0)
                if np.random.choice([0, 1], p=[1 - pbit, pbit]):
                    psi[i].x(0)
                if np.random.choice([0, 1], p=[1 - pphase, pphase]):
                    psi[i].z(0)
            else:
                psi[i].z(0)
                if np.random.choice([0, 1], p=[1 - pbit, pbit]):
                    psi[i].x(0)
                if np.random.choice([0, 1], p=[1 - pphase, pphase]):
                    psi[i].z(0)
    return psi

def zk_mod(psi, p):
    '''
    Alice Zero-Knowledge momdifications to the state |psi>.
    '''
    if len(psi) != len(p):
        raise ValueError('Same number of qubits and bits expected.')
    for i in range(len(psi)):
        if p[i] == 1:
            psi[i].h(0)
            if np.random.choice([0, 1], p=[1 - pbit, pbit]):
                psi[i].x(0)
            if np.random.choice([0, 1], p=[1 - pphase, pphase]):
                psi[i].z(0)
    return psi

def measurements(psi, basis):
    '''
    Alice measures using the secret basis.
    '''
    if len(psi) != len(basis):
        raise ValueError('Same number of qubits and basis expected.')
    results = []
    for i in range(len(psi)):
        if basis[i] == 1:
            psi[i].h(0)
            if np.random.choice([0, 1], p=[1 - pbit, pbit]):
                psi[i].x(0)
            if np.random.choice([0, 1], p=[1 - pphase, pphase]):
                psi[i].z(0)
        psi[i].measure(0, 0)
        psi[i] = transpile(psi[i], sim)
        exec = sim.run(psi[i], shots=1).result()
        result = int(list(exec.get_counts(psi[i]).keys())[0])
        results.append(result)
    return results

def c_aprox_gen(results, p, w):
    '''
    Generation of the approximation c' for c.
    '''
    c_aprox = []
    for i, bit in enumerate(results):
        # if bit == w[i] gamma[i]; else !gamma[i]
        decission = int(p[i] ^ (bit != w[i]))
        c_aprox.append(decission)
    return c_aprox

def equal_entries_percentage(list1, list2):
    '''
    Percentage of equal entries.
    '''
    if len(list1) != len(list2):
        raise ValueError("The lists must have the same length.")
    equals = 0
    for (a, b) in zip(list1, list2):
        equals += int(a == b)
    return (equals / len(list1)) * 100

def random_binary_string(length):
    '''
    Pseudo random binary strings.
    '''
    return [random.choice([0, 1]) for _ in range(length)]

def loading_bar(iteration, total, start_time, prefix='Progress:', length=50, fill='█', print_end='\r'):
    """
    Progress bar.
    """
    percent = 100 * (iteration / total)
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    elapsed_time = time.time() - start_time
    print(f'\r{prefix} |{bar}| {percent:.1f}% Elapsed: {elapsed_time:.1f}s', end=print_end)
    if iteration == total:
        print()

#----------------------------------------
# Protocol execution
#----------------------------------------
if __name__=='__main__':

    key_length = int(sys.argv[1])
    num_iter = int(sys.argv[2])
    pbit = float(sys.argv[3])  # Probability for bit-flip
    pphase = float(sys.argv[4])  # Probability for phase-flip
    sim = AerSimulator()

    percentages = []

    start_time = time.time()

    basis = quantum_random_binary_string(key_length)
    w = quantum_random_binary_string(key_length)


    iter=1
    for i in range(num_iter):
        dec = random.choice([0, 1])
        # 1. Keys generation (this keys could be shared through QKD)

        # 2. Preparation of the challenge (Bob)
        psi = psi_gen(w, basis) # |psi> state generation from w and basis

        c = quantum_random_binary_string(key_length) # Random generation for c
        psi = challenge_gen(psi, c, basis) # Challenge setup

        # After this, Bob sends the modified qubits to Alice 
        for i in range(len(psi)):
            if np.random.choice([0, 1], p=[1 - pbit, pbit]):
                psi[i].x(0)
        for i in range(len(psi)):
            if np.random.choice([0, 1], p=[1 - pphase, pphase]):
                psi[i].z(0)

        if dec == 0:
            # Honest prover Alice

            # 3. Zero-Knowledge modifications (Alice)
            p = quantum_random_binary_string(key_length) # Random generation for p
            psi = zk_mod(psi, p)

            # 4. Measurments (Alice)
            results = measurements(psi, basis) # Alice measures |psi> using the basis

            # 5. Building the approximation for c (Alice)
            c_aprox = c_aprox_gen(results, p, w)
            # After this, Alice sends her approximation of c to Bob

            # 6. Coincidence percentage (Bob)
            equal_percentage = equal_entries_percentage(c, c_aprox)
            percentages.append((equal_percentage, dec))

        else:
            # Dishonest prover Eve
            c_aprox = random_binary_string(key_length)
            equal_percentage = equal_entries_percentage(c, c_aprox)
            percentages.append((equal_percentage, dec))
        loading_bar(iter, num_iter, start_time)
        iter +=1

    #----------------------------------------
    # Data
    #----------------------------------------
    equal_percentages = [x[0] for x in percentages]
    decisions = [x[1] for x in percentages]

    iters = range(1,num_iter + 1)
    results = pd.DataFrame({'Iteration': iters, 'Decision': decisions, 'Percentages': equal_percentages})
    results.to_csv(f'iter_flip_error_data_{key_length}_{num_iter}.csv', index=False)

    # Separate honest iteration and dishonest iterations
    honest_data = [percentage for percentage, dec in percentages if dec == 0]
    dishonest_data = [percentage for percentage, dec in percentages if dec == 1]
    
    # Count values
    count_honest = pd.Series(honest_data).value_counts()
    count_dishonest = pd.Series(dishonest_data).value_counts()

    # Convert to DataFrame
    df_honest = pd.DataFrame({'Percentage': count_honest.index, 'Frecuency': count_honest.values})
    df_dishonest = pd.DataFrame({'Percentage': count_dishonest.index, 'Frecuency': count_dishonest.values})

    # Save to CSV
    df_honest.to_csv(f'honest_flip_error_data_{key_length}_{num_iter}.csv', index=False)
    df_dishonest.to_csv(f'dishonest_flip_error_data_{key_length}_{num_iter}.csv', index=False)
