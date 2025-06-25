from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
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

def psi_gen(a, b):
    '''
    Generation of the quantum state |psi>.
    '''
    if len(a) != len(b):
        raise ValueError('Same number of basis and bits expected.')
    psi = []
    for i in range(len(w)):
        qubit = QuantumCircuit(1, 1)
        if a[i] == 1:
            qubit.x(0)
        if b[i] == 1:
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
            else:
                psi[i].z(0)
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
    verbose = False
    if len(sys.argv) == 3:
        if str(sys.argv[2]) == 'v':
            verbose = True

    # 2. Preparation of the challenge (Bob)
    psi = psi_gen(w, basis) # |psi> state generation from w and basis

    c = quantum_random_binary_string(key_length) # Random generation for c
    psi = challenge_gen(psi, c, basis) # Challenge setup

    # After this, Bob sends the modified qubits to Alice 

    # 3. Zero-Knowledge modifications (Alice)
    p = quantum_random_binary_string(key_length) # Random generation for p
    psi = zk_mod(psi, p)

    # 4. Measurments (Alice)
    results = measurements(psi, basis) # Alice measures |psi> using the basis

    # 5. Building the approximation for c (Alice)
    c_aprox = c_aprox_gen(results, p, w)
    proof_state = psi_gen(tuple(a ^ b for a, b in zip(basis, c_aprox)), w)
    # After this, Alice sends her approximation of c to Bob

    # 6. Coincidence precentage (Bob)
    prove = measurements(proof_state, w)
    c_aprox = tuple(a ^ b for a, b in zip(prove, basis))
    equal_percentage = equal_entries_percentage(c, c_aprox)

    if verbose:

        print('\n--- Random Shared Secret Keys ---')
        print(f'Secret bits ---> a = {w}')
        print(f'Secret basis ---> b = {basis}\n')
        secret_state =  [w_val if b_val == 0 else ('+' if w_val == 0 else '-') for w_val, b_val in zip(w, basis)]
        print(f'Coded secret state ---> {secret_state}\n')
        input()

        print(f'--- Challenge Generation ---')
        challenge_state = [s_val if c_val == 0 else ({0: 1, 1: 0, '+': '-', '-': '+'}[s_val]) for s_val, c_val in zip(secret_state, c)]
        print(f'Random challenge sequence ---> c = {c}')
        print(f'Challenge state ---> {challenge_state}')
        input()

        print('\n--- Bob Sends challenge State through Quantum Channel to Alice --- \n')
        print('--- Alice\'s Zero Knowledge Modifications ---')
        print(f'Zero modifications sequence ---> p = {p}')
        mod_state =  [s_val if c_val == 0 else ({0: '+', 1: '-', '+': 0, '-': 1}[s_val]) for s_val, c_val in zip(challenge_state, p)]
        print(f'Modified state ---> {mod_state}')
        input()

        print('\n--- Alice\'s meassurements results and proof generation')
        print(f'Measure results ---> a\' = {results}')
        print(f'Generated approximation ---> c\' = {c_aprox}\n')
        proof_state = [w_val if b_val == 0 else ('+' if w_val == 0 else '-') for w_val, b_val in zip(tuple(a ^ b for a, b in zip(basis, c_aprox)), w)]
        print(f'Proof state ---> {proof_state}')
        input()

        print('\n--- Alice sends the proof state to Bob and he counts the coincidences between c and c\' ---')
        print(f'Numer of coincidences ---> {int(equal_percentage*key_length/100)}')

    print(f'\n{equal_percentage}% accuracy for {key_length} bits keys length.\n')
