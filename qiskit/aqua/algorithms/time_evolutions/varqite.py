# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""The Variational Quantum Time Evolution Interface"""

import warnings
from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict

import numpy as np

from qiskit.circuit import ParameterExpression, ParameterVector
from qiskit.aqua.operators import StateFn, OperatorBase, NaturalGradient, CircuitQFI, \
    CircuitGradient

from .varqte import VarQTE


class VarQITE(VarQTE):
    """Variational Quantum Imaginary Time Evolution.
       https://doi.org/10.22331/q-2019-10-07-191

    Algorithms that use McLachlans variational principle to compute the imaginary time evolution
    for a given Hermitian operator (Hamiltonian) and quantum state.
        ∑ _j Re(A_i,j) dθ_j/dt = -Re(C_i)
    """

    @abstractmethod
    def _prepare_op(self, operator: OperatorBase) -> OperatorBase:
        """
        Prepare the operator that is needed for the respective time evolution
        Args:
            operator: Operator by which the state shall be evolved

        Returns:
            Adpated operator which is needed for the time evolution itself.

        """
        return operator
