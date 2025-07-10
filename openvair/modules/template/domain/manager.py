"""Module for managing template domain operations.

This module provides the entry point for managing template domain operations.
It starts an RPC server to consume messages related to template management.

Classes:
    - TemplateFactory: Factory class for creating template instances.

Dependencies:
    - MessagingServer: Handles message-based communication.
    - SERVICE_LAYER_DOMAIN_QUEUE_NAME: Queue name for service layer domain
        communication.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.template.config import SERVICE_LAYER_DOMAIN_QUEUE_NAME
from intakevms.modules.template.domain import model
from intakevms.libs.messaging.messaging_agents import MessagingServer

LOG = get_logger('domain-manager')

if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    server = MessagingServer(
        queue_name=SERVICE_LAYER_DOMAIN_QUEUE_NAME,
        manager=model.TemplateFactory(),
    )
    server.start()
