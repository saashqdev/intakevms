"""Module for managing virtual network domain operations.

This module provides the entry point for managing virtual network domain
operations. It starts an RPC server to consume messages related to virtual
networks.

Classes:
    - VirtualNetworkFactory: Factory class for creating virtual network
        instances.

Dependencies:
    - Protocol: Messaging protocol for communication.
    - SERVICE_LAYER_DOMAIN_QUEUE_NAME: Queue name for service layer domain
        communication.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.virtual_network.config import (
    SERVICE_LAYER_DOMAIN_QUEUE_NAME,
)
from intakevms.modules.virtual_network.domain import model
from intakevms.libs.messaging.messaging_agents import MessagingServer

LOG = get_logger('domain-manager')


if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    server = MessagingServer(
        queue_name=SERVICE_LAYER_DOMAIN_QUEUE_NAME,
        manager=model.VirtualNetworkFactory(),
    )
    server.start()
