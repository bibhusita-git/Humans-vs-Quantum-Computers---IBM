# Womainium IBM Challenge 2022: Humans vs. Quantum Computers

**Task  Given:** Create a working interactive ‘program’ (it can be a website, game, app, etc.) in which a human user is facing off against a quantum computer. This is broad on purpose - the program can be built in many different ways. Your program should implement strategies that seriously challenge the human player. The implementation must utilize more than just probabilities related to measuring quantum states. You must use Qiskit to program the computer’s gameplay strategy, and as much as possible, the strategy should be implemented with quantum circuits and quantum gates on real quantum hardware (although using the Simulator is understandable given the time limit).

## Quantum Permutation Algorithm and Secret Sharing 

The **`QuantumPermutations`** directory contains all materials required for implmenting the secret sharing algorithm . It is recommended to go thtough the tutorial file **`Tutorial_QPSS.ipynb`** before moving ahead. The directory contains the following files,

- The **`quantum_permutation_utils.py`** file has the all necessary imports and and other utility functions defined by us necessary to facilitate the implmentation.
- The **`Tutorial_QPSS.ipynb`** file is a self-contained tutorial on the secret sharing protocol. The structure of the tutorial is as follows
    - The **Generating Permutations on Quantum Computers** section gives a short intorduciton to our quantum algorithm of creating an equal superposition of permutations. We give some example implementations fo cases with few qubits and also describe the general procedure for arbitrary number of states
    - The **Applications to Secret Sharing** section describes how the permutation generation procedure could be used for Secret Sharing.
    - In **Drawbacks and Possible Workarounds** we mention the drawabacks of our algorithm that limits its practical utility and also discuss possible ways using which this protocol could be used to made more robust.   

## About Game: QuantumV

We are trying to integrate the above Algorithm with a side-scroller game: QuantumV. The game is planed to have many chapters each containing some Quantum Challenge for the player to win.

You can play the game by running the **`main.py`** file in **Game/code** folder.

## Game Story: QuantumV

Sandhanam is a Indian chemist who worked on a chemical formula in his college days which is 50x powerful than Marijuana — ‘Blue Crystal’.

Sandhanam now is selling copies of his formula to top Drug Mafia of Asia and Africa. Till now he has made deal with 9 underworlds: 

Sandhanam is planning to send these copies through his brothers.

Vikram has managed to discover that Sandhanam is using a special quantum algorithm to encrypt the password for locker having original paper and Sandhanam distribute the keys to his 9 brothers(all quantum software engineers - just for matching theme ;-] ) who will deliver the formula. 

Vikram has to stop the containers to reach their destination and open the main locker (which is only possible if he manages to know the keys from Sandhanam’s brothers) and destroy the original paper of the formula and ultimately kill Sandhanam. (No one knows the location of Sandhanam and his headquarter.)


**Chapter 1:** Meeting Aryam (having key for first ancilla qubit)

Aryam (youngest brother of Sandhanam) lives in Tawang and is planning to cross India-Mayanmar border through district of Anjaw. Vikram manages stop Aryam in Anjaw. Aryam challenges Vikram if he could pass the Quantum Game designed by him. Then only he will tell first key to him.

In Aryam's Quantum Game, he is shooting qubit balls in different states(q1), Vikram has to destroy them by shooting qubit balls of state X(q1) and reach Aryam.

**Chapter 2:** Arjundas’s Challenge

Arjundas(another brother of Sandhanam) is travelling through Cruise from Bhavnagar(Gujrat) to Port Dubai. Vikram lands on Arjun’s ship where he is challenged to make a Quantum Operations from given set of gates.

**Chapter 3:** Beaking Rolex’s Pride

Rolex is based in Rangat(A & N). He is experimenting on a illegal quantum internet tower setup on a small island. Vikram has secretly …. 

**Game Story and Game Integration is not complete yet.**

## Contributors

**Quantum Algorithm:** Rajarsi Pal, Sandipan Manna

**Game Design:** Ashmit JaiSarita Gupta, Sujash Agrawal

**Readme and Game Story:** Samundra Saurav Kalita, Bibhusita Baishya
