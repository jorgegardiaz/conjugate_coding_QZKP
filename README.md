# Quantum Zero-Knowledge Proof based on Conjugate Coding

This repository contains an implementation of a **zero-knowledge** cryptographic protocol in a quantum setting, using libraries such as [Qiskit](https://qiskit.org/). The main goal is to demonstrate how to validate information (e.g., a secret bitstring and its basis) without revealing this secret itself, by leveraging quantum states.

## Table of Contents
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Script Usage](#script-usage)
  - [1. QZKP_barebones.py](#1-qzkp_barebonespy)
  - [2. QZKP_ideal.py](#2-qzkp_idealpy)
  - [3. QZKP_noise_damping.py](#3-qzkp_noise_dampingpy)
  - [4. QZKP_noise_flip.py](#4-qzkp_noise_flippy)
- [Technical Explanation](#technical-explanation)
  - [Quantum Key Generation](#quantum-key-generation)
  - [State Preparation](#state-preparation)
  - [Zero-Knowledge Modifications](#zero-knowledge-modifications)
  - [Measurements and Comparisons](#measurements-and-comparisons)
- [Possible Improvements](#possible-improvements)
- [Contributions](#contributions)
- [License](#license)

---

## Overview

This project explores a **Zero-Knowledge Proof (ZKP)** approach within the quantum paradigm. It leverages quantum states to prove the possession of certain information (like a secret bitstring and the basis in which it was encoded) without revealing the actual secret to the verifier.

The repository includes different scripts that illustrate various versions of the protocol:

- **Basic version** without noise.  
- **Versions with different noise models** (phase damping, bit-flip, phase-flip, etc.).  
- **A minimal example** to showcase the fundamental steps of the protocol (similar to BB84 for quantum key generation).

---

## Repository Structure

A suggested directory layout is as follows:

```bash
├── README.md                 # Project overview and instructions
├── requirements.txt          # List of dependencies (Qiskit, etc.)
├── src
│   ├── QZKP_barebones.py     # (formerly QZKP_BB84.py) Minimal or "barebones" example
│   ├── QZKP_ideal.py         # (formerly good_vs_bad.py) Ideal version without noise
│   ├── QZKP_noise_damping.py # (formerly good_vs_bad_error.py) With phase-amplitude noise
│   ├── QZKP_noise_flip.py    # (formerly good_vs_bad_error_flip.py) With bit-flip and phase-flip noise
└── docs
    └── ...                   # (Optional) Extended documentation, graphs, or reports
```

1. **`src/`**: Main folder containing the scripts that implement each version of the protocol.  
2. **`docs/`** *(optional)*: Holds additional documentation, reports, and images if you need more extensive explanations or visualizations.

---

## Prerequisites

- [Python 3.8+](https://www.python.org/)
- [Qiskit](https://qiskit.org/) (including `qiskit-aer`, `qiskit-terra`, etc.)
- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)

All dependencies are (or can be) listed in the `requirements.txt` file.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```
2. *(Optional)* **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Script Usage

### 1. `QZKP_barebones.py`
A **minimal** script that shows the fundamental protocol steps:
```bash
python QZKP_barebones.py <key_length>
```
It prints the percentage of correctly guessed challenge bits (the “success rate”) for a given key length.

### 2. `QZKP_ideal.py`
An **ideal** version (no noise) that compares a *honest* prover (Alice) and a *dishonest* one (Eve):
```bash
python QZKP_ideal.py <key_length> <num_iterations>
```
Generates CSV files with statistics for the success rate of each iteration, distinguishing honest vs. dishonest attempts.

### 3. `QZKP_noise_damping.py`
Implements a **phase-amplitude damping** noise model:
```bash
python QZKP_noise_damping.py <key_length> <num_iterations>
```
Saves CSVs with results for honest and dishonest prover outcomes under damping noise.

### 4. `QZKP_noise_flip.py`
Implements **bit-flip** and **phase-flip** noise models:
```bash
python QZKP_noise_flip.py <key_length> <num_iterations>
```
Similar data output to the other scripts, generating CSVs with per-iteration metrics.

---

## Possible Improvements
- **Multi-qubit optimization**: Currently, each qubit is handled individually. You could explore managing full quantum registers to optimize performance.
- **Additional statistical analyses**: Integrate deeper tests (e.g., hypothesis testing) to confirm quantum advantage or measure security more rigorously.
- **Enhanced visualizations**: Add scripts to visualize distributions of success rates under different noise levels and key lengths.

---

## Contributions
Contributions are welcome! To propose changes:
1. Fork this repository
2. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/new-functionality
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new functionality or fix bug XYZ'
   ```
4. Submit a Pull Request and describe the changes in detail.

---

## License
This project is available under the MIT License. See the file [LICENSE](LICENSE) for more information.
