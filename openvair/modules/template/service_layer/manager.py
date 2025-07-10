"""Service layer manager for the template module.

This module provides the entry point for managing template service operations.
It starts an RPC server to handle service layer requests.

Classes:
    - TemplateServiceLayerManager: Manager for handling template-related tasks.

Dependencies:
    - MessagingServer: Handles message-based communication.
    - API_SERVICE_LAYER_QUEUE_NAME: Queue name for API service layer
        communication.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.template.config import API_SERVICE_LAYER_QUEUE_NAME
from intakevms.libs.messaging.messaging_agents import MessagingServer
from intakevms.modules.template.service_layer.services import (
    TemplateServiceLayerManager,
)

LOG = get_logger('service-layer-manager')


if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    service = TemplateServiceLayerManager
    service.start(block=False)
    server = MessagingServer(
        queue_name=API_SERVICE_LAYER_QUEUE_NAME,
        manager=service,
    )
    server.start()
