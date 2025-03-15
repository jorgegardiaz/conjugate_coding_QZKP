from qiskit import QuantumCircuit # qiskit 1.3.1
from qiskit_aer import AerSimulator # qiskit_aer 0.16.0
import sys

#----------------------------------------
# Funcitons
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
        if basis[i] == 1:
            qubit.h(0)
        psi.append(qubit)
    return psi

def challenge_gen(psi, c):
    '''
    Generation of the challenge for |psi>.
    '''
    if len(psi) != len(c):
        raise ValueError('Same number of qubits and bits expected.')
    for i in range(len(psi)):
        if c[i] == 1:
            psi[i].h(0)
    return psi

def zk_mod(psi, p):
    if len(psi) != len(p):
        raise ValueError('Same number of qubits and bits expected.')
    for i in range(len(psi)):
        if p[i] == 1:
            psi[i].h(0)
    return psi

def measurements(psi, basis):
    if len(psi) != len(basis):
        raise ValueError('Same number of qubits and basis expected.')
    results = []
    for i in range(len(psi)):
        if basis[i] == 1:
            psi[i].h(0)
        psi[i].measure(0, 0)
        exec = sim.run(psi[i], shots=1).result()
        result = int(list(exec.get_counts(psi[i]).keys())[0])
        results.append(result)
    return results

def c_aprox_gen(results, p, w):
    c_aprox = []
    for i, bit in enumerate(results):
        # if bit == w[i] gamma[i]; else !gamma[i]
        decission = int(p[i] ^ (bit != w[i]))
        c_aprox.append(decission)
    return c_aprox

def equal_entries_percentage(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("The lists must have the same length.")
    equals = 0
    for (a, b) in zip(list1, list2):
        equals += int(a == b)
    return (equals / len(list1)) * 100

#----------------------------------------
# Protocol execution
#----------------------------------------
if __name__ == '__main__':
    
    sim = AerSimulator()
    key_length = int(sys.argv[1])
    basis = quantum_random_binary_string(key_length)
    w = quantum_random_binary_string(key_length)

    # 2. Preparation of the challenge (Bob)
    psi = psi_gen(w, basis) # |psi> state generation from w and basis

    c = quantum_random_binary_string(key_length) # Random generation for c
    psi = challenge_gen(psi, c) # Challenge setup

    # After this, Bob sends the modified qubits to Alice 

    # 3. Zero-Knowledge modifications (Alice)
    p = quantum_random_binary_string(key_length) # Random generation for p
    psi = zk_mod(psi, p)

    # 4. Measurments (Alice)
    results = measurements(psi, basis) # Alice measures |psi> using the basis

    # 5. Building the approximation for c (Alice)
    c_aprox = c_aprox_gen(results, p, w)

    # After this, Alice sends her approximation of c to Bob

    # 6. Coincidence precentage (Bob)
    equal_percentage = equal_entries_percentage(c, c_aprox)

    print(f'{equal_percentage}% accuracy for {key_length} bits key length.')
