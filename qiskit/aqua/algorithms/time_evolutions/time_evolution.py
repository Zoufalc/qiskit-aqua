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

"""The Time Evolution Interface"""

import warnings
from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict

import numpy as np

from qiskit.circuit import ParameterExpression, ParameterVector
from qiskit.aqua.operators import StateFn, OperatorBase


class TimeEvolution(ABC):
    """The Time Evolution Interface.

    Algorithms that can compute a time evolution for a given Hermitian operator (Hamiltonian) and
    quantum state.
    """
    def __init__(self, state: StateFn):
        """
        Initialize the time evolution algorithm
        Args:
            state:
        """
        self._state = state
        self._operator = None
        self._time = None
        self._parameters = None

    @property
    def state(self) -> StateFn:
        """
        Return state to be evolved
        """
        return self._state

    @state.setter
    def state(self, sf: StateFn):
        """
        Set state to be evolved
        """
        self._state = sf

    @property
    def operator(self) -> OperatorBase:
        """
        Return operator to evolve the state with
        """
        return self._operator

    @operator.setter
    def operator(self, op: OperatorBase):
        """
        Set operator to evolve the state with
        """
        self._operator = op

    @property
    def time(self) -> Union[float, int]:
        """
        Return the time for which the state is evolved with the operator
        """
        return self._time

    @time.setter
    def time(self, t: Union[float, int]):
        """
        Set the time for which the state is evolved with the operator
        """
        self._time = t

    @property
    def parameters(self) -> Union[ParameterExpression, List[ParameterExpression],
                                          ParameterVector]:
        """
        Return the current parameters of the quantum state
        """
        return self._parameters

    @parameters.setter
    def parameters(self, params: Union[ParameterExpression, List[ParameterExpression],
                                   ParameterVector]):
        """
        Set the current parameters of the quantum state
        """
        self._parameters = params

    @abstractmethod
    def evolve(self,
               operator: OperatorBase,
               time: Union[float, int],
               parameters: Optional[Union[ParameterExpression, List[ParameterExpression],
                                          ParameterVector]] = None) -> StateFn:
        raise NotImplementedError
