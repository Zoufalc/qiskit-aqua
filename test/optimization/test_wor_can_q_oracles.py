import numpy as np

from qiskit import QuantumCircuit, IBMQ, Aer
from qiskit.aqua import QuantumInstance

from qiskit.ignis.mitigation.measurement import CompleteMeasFitter


# Initialize QuantumInstances
TOKEN = '41a450e0c5bf37ee6ffb442fb3cf07358fd5c2a291d8ae11c535af1ccb1e683d7e4cadf6c2ff24e0cd88e1cf286476a91ed' \
        '0a78d1a336a5ac363783196e48448'
IBMQ.save_account(TOKEN, overwrite=True)
provider = IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q-internal', group='deployed', project='default')

# backend_name = 'ibmq_paris'
backend_name = 'ibmq_johannesburg'
layout = [0, 1, 5, 6, 7]
qi_noise_model_ibmq = QuantumInstance(backend=provider.get_backend(backend_name), shots=8000,
                                      measurement_error_mitigation_cls=CompleteMeasFitter,
                                      skip_qobj_validation=False, initial_layout=layout, optimization_level=3)
qi_qasm = QuantumInstance(backend=Aer.get_backend('qasm_simulator'), optimization_level=2,
                          backend_options={"method": "density_matrix"},
                          seed_simulator=2, seed_transpiler=2, shots=8000)

# qc = QuantumCircuit(5)
# qc.ry(np.pi/2, range(5))
# for i in range(1,5):
#     qc.cry(-np.pi/2, i-1, i)
# qc.measure_all()

qc = QuantumCircuit(5)
qc.ry(np.pi/2, range(5))
for i in range(4,0,-1):
    qc.cry(-np.pi/2, i, i-1)
qc.measure_all()

result = qi_noise_model_ibmq.execute(qc)
print(result.get_counts())

