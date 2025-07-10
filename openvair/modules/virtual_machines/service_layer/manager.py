"""Module for managing the service layer of virtual machines.

This module initializes the ORM mappers, starts the service layer manager,
and sets up an RPC server for handling requests related to virtual machine
operations. The service layer manager handles the core business logic for
virtual machine operations and communicates with other components via RPC.

Classes:
    None

Functions:
    main: Initializes the ORM mappers, starts the service layer manager,
        and sets up the RPC server for handling requests.
"""

from intakevms.libs.log import get_logger
from intakevms.libs.messaging.messaging_agents import MessagingServer
from intakevms.modules.virtual_machines.config import (
    API_SERVICE_LAYER_QUEUE_NAME,
)
from intakevms.modules.virtual_machines.service_layer import services

LOG = get_logger('service-layer-manager')


if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    service = services.VMServiceLayerManager
    service.start(block=False)
    server = MessagingServer(
        queue_name=API_SERVICE_LAYER_QUEUE_NAME,
        manager=service,
    )
    server.start()
