"""Module for initializing the BlockDevice Service Layer Manager.

It imports necessary modules and initializes a Protocol instance with
server=True, indicating it is configured as a server for handling RPC messages.
The Protocol instance is initialized with specific parameters including the
queue name and an instance of model.InterfaceFactory() as the manager.

Modules:
    get_logger: Function to retrieve a logger instance from intakevms.libs.log
        module.
    Protocol: Class for handling messaging protocols
        from intakevms.libs.messaging.protocol module.
    SERVICE_LAYER_DOMAIN_QUEUE_NAME: Constant defining the queue name for
        domain service layer from intakevms.modules.block_device.config module.
    model: Module containing the InterfaceFactory class for creating block
        device interfaces.

Usage:
    This script is typically executed to start an RPC server that consumes
    messages for block device domain management.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.block_device.config import SERVICE_LAYER_DOMAIN_QUEUE_NAME
from intakevms.modules.block_device.domain import model
from intakevms.libs.messaging.messaging_agents import MessagingServer

LOG = get_logger('domain-manager')


if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    server = MessagingServer(
        queue_name=SERVICE_LAYER_DOMAIN_QUEUE_NAME,
        manager=model.InterfaceFactory(),
    )
    server.start()
