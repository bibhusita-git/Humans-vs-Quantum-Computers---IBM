###########################################################################################
                                        ## imports ##
###########################################################################################



import numpy as np
from numpy import pi
import math
import seaborn as sns
from IPython.display import Image
import matplotlib.pyplot as plt
from typing import Union

from qiskit import *
from qiskit.circuit.library import *
from qiskit.algorithms import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit #, InstructionSet
from qiskit import quantum_info, IBMQ, Aer
from qiskit.quantum_info import partial_trace, Statevector, state_fidelity
from qiskit.utils import QuantumInstance
from qiskit.extensions import HamiltonianGate
from qiskit.circuit.quantumregister import Qubit
from qiskit.visualization import plot_histogram, plot_state_qsphere, plot_bloch_multivector, plot_bloch_vector

qsm = Aer.get_backend('qasm_simulator')
stv = Aer.get_backend('statevector_simulator')
aer = Aer.get_backend('aer_simulator')


##################################################################################################
                                    ## helper functions ##
##################################################################################################

s

def measure_and_plot(qc: QuantumCircuit, show_counts:bool= False, measure_ancilla: bool = False, ancilla_specifier:Union[int, str] = 'all'):
    """ Measure and plot the state of the data registers, optionally measure the control ancillas. 
        
        ARGS:
            qc : 'QuantumCircuit' -> to be measured
            show_counts : 'bool' -> print the counts dictionary
            measure_ancilla : 'bool' ->  indicates whether to measure the control ancilla registers.
            ancilla_specifier : 'int' -> inidicates whihch of the conteol registers to meausure, 
                                            for eg. ancilla_specifier= 1 refers to the first control ancilla
                                                    ancilla_specifier= 'all' refers to all the ancillas                                                           
        RETURNS:
            plots histogram over the computational basis states

     """
    qc_m = qc.copy()
    creg = ClassicalRegister( len(qc_m.qregs[0]) )
    qc_m.add_register(creg)
    qc_m.measure(qc_m.qregs[0], creg)

    if measure_ancilla== True:

        if isinstance(ancilla_specifier, int):
            if ancilla_specifier > len(qc_m.qregs) or ancilla_specifier < 1: raise ValueError(" 'ancilla_specifier' should be less than no. of control registers and greater than 0")

            creg_cntrl = ClassicalRegister(len(qc_m.qregs[ancilla_specifier]))
            qc_m.add_register(creg_cntrl)
            qc_m.measure(qc_m.qregs[ancilla_specifier], creg_cntrl )

        elif isinstance(ancilla_specifier, str) and ancilla_specifier== "all":
            for reg in qc_m.qregs[1:] :
                creg = ClassicalRegister(len(reg))
                qc_m.add_register(creg)
                qc_m.measure(reg, creg)
                
    plt.figure()
    counts = execute(qc_m, qsm, shots= 1024).result().get_counts()
    if show_counts== True: print(counts)
    return plot_histogram(counts)
    

## initial state preparation ~
def s_psi0(p):
    """ Prepare a QuantumCircuit that intiates a state required
        input:
            p= amplitude 
        output:
            s_psi0 gate    """
            
    qc = QuantumCircuit(1, name= " S_psi0 ")
    theta = 2*np.arcsin(np.sqrt(p))
    qc.ry(theta, 0)

    return qc.to_gate()    

## string to oracle ~
def str_to_oracle(pattern: str, name= 'oracle', return_type = "QuantumCircuit" ) -> Union[QuantumCircuit,  Statevector] :
    """ Convert a given string to an oracle circuit
        ARGS:
             pattern: a numpy vector with binarry entries 
             return_type: ['QuantumCircuit', 'Statevector']

        RETURNS: 
               'QuantumCircuit' implementing the oracle
               'Statevector' evolved under the action of the oracle   """


    l = len(pattern)
    qr = QuantumRegister(l, name='reg')
    a = AncillaRegister(1, name='ancilla')
    oracle_circuit = QuantumCircuit(qr, a, name= name+'_'+ pattern )
    for q in range(l):
        if(pattern[q]=='0'): oracle_circuit.x(qr[q])
    oracle_circuit.x(a)
    oracle_circuit.h(a)
    oracle_circuit.mcx(qr, a)
    oracle_circuit.h(a)
    oracle_circuit.x(a)
    for q in range(l):
        if(pattern[q]=='0'): oracle_circuit.x(qr[q])
    
    #oracle_circuit.barrier()
    if return_type == "QuantumCircuit":
        return oracle_circuit
    elif return_type == "Statevector":
        return Statevector.from_instruction(oracle_circuit)



## oracle prep ~
def generate_oracles(good_states: list) -> QuantumCircuit :
    """ Return a QuantumCircuit that implements the oracles given the good_states
        ARGS:
            good_states: list of good staes, states must be binary strings, Eg. ['00', '11']

        RETURNS:
           ' QuantumCircuit' iplementing the oracle circuits """

    oracles = [ str_to_oracle(good_state) for good_state in good_states ]
    oracle_circuit = oracles[0]
    for oracle in oracles[1:] :
        oracle_circuit.compose(oracle,  inplace= True)
    

    return oracle_circuit

## diffuser prep ~
def diffuser(l:int)-> QuantumCircuit :
    """ Generate the Diffuser operator for the case where the initial state  is 
        the equal superposition state of all basis vectors 

        ARGS:
            l: no. of data qubits
        
        RETRUNS:
                QuantumCircuit

    """

    qr = QuantumRegister(l, name='reg')
    a = AncillaRegister(1, name='ancilla')
    circuit = QuantumCircuit(qr, a, name= 'Diff.')
    
    circuit.h(qr)
    circuit.x(qr)
    
    circuit.x(a)
    circuit.h(a)
    circuit.mcx(qr ,a)
    circuit.h(a)
    circuit.x(a)

    circuit.x(qr)
    circuit.h(qr)
          
    return circuit

## grover prep ~
def grover(good_states: list, insert_barrier:bool= False)-> QuantumCircuit:
    
    oracle_circuit = generate_oracles(good_states)

    num_qubits= oracle_circuit.num_qubits - oracle_circuit.num_ancillas
    diffuser_circuit = diffuser(num_qubits)
    if insert_barrier== True: oracle_circuit.barrier()
    oracle_circuit.compose(diffuser_circuit, inplace= True)

    return oracle_circuit



####################################################################################################
                                ## permutation routines ##
####################################################################################################

def bit_conditional( num: int, qc: QuantumCircuit, register: QuantumRegister): ## @helper_function
    """ helper function to assist the conditioning of ancillas 
    
        ARGS:
            num : the integer to be conditioned upon 
            qc : QuantumCircuit of the original circuit
            register : QuantumRegister corresponding to the ancilla which is conditioned upon 
        
        RETURNS:
            Works inplace i.e modifies the original circuit 'qc' that was passed """

    n = len(register)
    bin_str = format(num, "b").zfill(n)
    assert len(bin_str) == len(register)            ## need to assurethe bit ordering covention according tto qiskit's

    bin_str = bin_str[::-1]                         ## reverse the bit string
    for index, bit in enumerate(bin_str):
        if bit== '0': qc.x(register[index]) 
        

def generate_permutation_operators(num_bits:int , power:int= 1)-> QuantumCircuit :
    """ Function to generate the permutaion operators 
    
        ARGS:
            num_bits : no. of elements in the permutation set
            power : power of the permuation operator
            
        RETURNS:
            QuantumCircuit implementing the permutation operator
    """

    if num_bits < 2 : raise ValueError(" 'num_bits' must be greater than or equal to 2 ") 
    if power not in list(range(num_bits)) : raise ValueError(" 'power' must be such that ; 0 <= 'power' < 'num_bits'  ")

    qreg = QuantumRegister(num_bits, name= 'qreg')
    qc = QuantumCircuit(qreg)

    for rep in range(power):    
        for qubit in range(num_bits-1):
            qc.swap(qubit, qubit+1)

    return qc.to_gate(label= 'P_'+str(num_bits)+'('+str(power)+')')

