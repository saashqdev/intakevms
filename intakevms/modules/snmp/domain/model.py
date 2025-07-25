"""Factory pattern for creating SNMP agents.

This module defines the `AbstractSNMPFactory` and `SNMPFactory` classes,
which are responsible for creating SNMP agents based on the specified type.

Classes:
    AbstractSNMPFactory: Abstract factory for creating SNMP agents.
    SNMPFactory: Concrete factory for creating SNMP agents.
"""

import abc
from typing import ClassVar, cast

from intakevms.modules.snmp.domain.base import BaseSNMP
from intakevms.modules.snmp.domain.agentx import agentx
from intakevms.modules.snmp.domain.exceptions import SNMPAgentTypeError


class AbstractSNMPFactory(metaclass=abc.ABCMeta):
    """Abstract factory for creating SNMP agents.

    This abstract factory defines the interface for creating
    SNMP agents of various types.
    """

    @abc.abstractmethod
    def get_snmp_agent(self, snmp_type: str) -> BaseSNMP:
        """Create an SNMP agent of the specified type.

        Args:
            snmp_type (str): The type of SNMP agent to create.

        Returns:
            BaseSNMP: An instance of an SNMP agent.
        """
        ...


class SNMPFactory(AbstractSNMPFactory):
    """Concrete factory for creating SNMP agents.

    This factory creates SNMP agents of different types based on the provided
    type identifier.
    """

    _snmp_classes: ClassVar = {
        'agentx': agentx.SNMPAgentx,
    }

    def get_snmp_agent(self, snmp_type: str) -> BaseSNMP:
        """Create an SNMP agent of the specified type.

        Args:
            snmp_type (str): The type of SNMP agent to create.

        Returns:
            BaseSNMP: An SNMP agent object of the specified type.

        Raises:
            SNMPAgentTypeError: If the specified SNMP agent type is not found.
        """
        try:
            snmp_class = self._snmp_classes[snmp_type]
        except KeyError:
            message = f"SNMP type '{snmp_type}' not found"
            raise SNMPAgentTypeError(message)
        else:
            return cast(BaseSNMP, snmp_class())
