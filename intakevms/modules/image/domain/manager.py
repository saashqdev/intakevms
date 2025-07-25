"""Domain manager for the image service.

This script initializes and starts the RPC server for handling image-related
operations in the domain layer. It listens for incoming requests on the
specified queue and delegates them to the appropriate handlers.

Usage:
    Run this script to start the domain-layer manager.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.image.config import SERVICE_LAYER_DOMAIN_QUEUE_NAME
from intakevms.modules.image.domain import model
from intakevms.libs.messaging.messaging_agents import MessagingServer

LOG = get_logger('domain-manager')


if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    server = MessagingServer(
        queue_name=SERVICE_LAYER_DOMAIN_QUEUE_NAME,
        manager=model.ImageFactory(),
    )
    server.start()
