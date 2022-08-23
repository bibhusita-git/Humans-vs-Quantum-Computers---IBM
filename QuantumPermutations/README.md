#### Quantum Permutation Algorithm and Secret Sharing 

The **`QuantumPermutations`** directory contains all materials required for implmenting the secret sharing algorithm . There are two files in this directory 

- The **`quantum_permutation_utils.py`** file has the all necessary imports and and other utility functions defined by us necessary to facilitate the implmentation.
- The **`Tutorial_QPSS.ipynb`** file is a self-contained tutorial on the secret sharing protocol. The structure of the tutorial is as follows
    - The **Generating Permutations on Quantum Computers** section gives a short intorduciton to our quantum algorithm of creating an equal superposition of permutations. We give some example implementations fo cases with few qubits and also describe the general procedure for arbitrary number of states
    - The **Applications to Secret Sharing** section describes how the permutation generation procedure could be used for Secret Sharing.
    - In **Drawbacks and Possible Workarounds** we mention the drawabacks of our algorithm that limits its practical utility and also discuss possible ways using which this protocol could be used to made more robust.   
