# from qiskit.quantum_info import Pauli
# from qiskit.aqua.operators import PauliOp
# from qiskit.aqua.operators import StateFn, AerPauliExpectation, CircuitSampler
# from qiskit import Aer, QuantumCircuit
#
# #backend
# backend = Aer.get_backend('statevector_simulator')
#
#
# #operator
# pauli = Pauli.from_label('Z'*2)
# pauli = PauliOp(pauli)
#
# #state
# my_state = QuantumCircuit(2)
# my_state.h(0)
#
# #eval
# meas = ~StateFn(pauli) # ~ is the same as .adjoint()
# expect_op = meas @ StateFn(my_state)
# # I can already call eval() on expect_op, but it will do the evaluation by matrix multiplication. Here, convert to AerPauli measurement
# aer_expect_op = AerPauliExpectation().convert(expect_op)
# executed_op = CircuitSampler(backend=backend).convert(aer_expect_op)
# expectation_value = executed_op.eval()

from qiskit.quantum_info import Pauli
from qiskit.aqua.operators import PauliOp
from qiskit.aqua.operators import StateFn, PauliExpectation, CircuitSampler
from qiskit import Aer, QuantumCircuit
#backend
backend = Aer.get_backend('statevector_simulator')
#operator
pauli = Pauli.from_label('Z'*2)
pauli = PauliOp(pauli)
#state
my_state = QuantumCircuit(2)
my_state.h(0)
#eval
meas = ~StateFn(pauli) # ~ is the same as .adjoint()
expect_op = meas @ StateFn(my_state)

aer_expect_op = PauliExpectation().convert(expect_op)
executed_op = CircuitSampler(backend=backend).convert(aer_expect_op)
# Gives expectation value
expectation_value = executed_op.eval()
# Gives probabilities for measurements
op = executed_op.oplist[-1]
probabilities = op.primitive.probabilities()
