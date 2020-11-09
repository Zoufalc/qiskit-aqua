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

from .time_evolution import TimeEvolution


class VarQTE(TimeEvolution):
    """Variational Quantum Time Evolution.
       https://doi.org/10.22331/q-2019-10-07-191

    Algorithms that use McLachlans variational principle to compute a time evolution for a given
    Hermitian operator (Hamiltonian) and quantum state.
    """
    def __init__(self, state: StateFn):
        """
        Initialize the time evolution algorithm
        Args:
            state:
        """
        super().__init__(state)
        self._qfi_method = 'lin_comb_full'
        self._grad_method = 'lin_comb'
        self._regularization = 'ridge'

    @abstractmethod
    def _prepare_op(self, operator: OperatorBase) -> OperatorBase:
        """
        Prepare the operator that is needed for the respective time evolution
        Args:
            operator: Operator by which the state shall be evolved

        Returns:
            Adpated operator which is needed for the time evolution itself.

        """
        raise NotImplementedError

    def evolve(self,
               operator: OperatorBase,
               time: Union[float, int],
               num_time_steps: int,
               parameters: Optional[Union[ParameterExpression, List[ParameterExpression],
                                          ParameterVector]] = None,
               parameter_values: Optional[List[float]] = None,
               qfi_method: Optional[Union[str, CircuitQFI]] = None,
               grad_method: Optional[Union[str, CircuitGradient]] = None,
               regularization: Optional[Union[str, callable]] = None) -> StateFn:
        self._operator = operator
        self._time = time
        self._parameters = parameters
        if qfi_method:
            self._qfi_method = qfi_method
        if grad_method:
            self._grad_method = grad_method
        if regularization:
            # TODO enable the use of custom regularization methods
            self._regularization = regularization

        # Convert the operator that holds the Hamiltonian and ansatz into a NaturalGradient operator
        nat_grad = NaturalGradient(qfi_method=self._qfi_method, grad_method=self._grad_method,
                                   regularization=self._regularization
                                   ).convert(self._prepare_op(self._operator), self._parameters)

        # Propagate the Ansatz parameters step by step according to the explicit Euler method
        self._parameter_values = parameter_values
        for j in range(num_time_steps):
            param_dict = dict(zip(self._parameters, self._parameter_values))
            nat_grad_result = np.real(nat_grad.assign_parameters(param_dict).eval())
            self._parameter_values = list(np.subtract(self._parameter_values, time /
                                                      num_time_steps * np.real(nat_grad_result)))

        return self._state.assign_parameters(dict(zip(parameters, self._parameter_values)))

    def error_bound(self):
        #TODO check if this is equivalent for real and imaginary

        return