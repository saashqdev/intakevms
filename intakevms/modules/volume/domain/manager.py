"""Module for managing the volume domain layer.

This module provides the entry point for managing the volume domain layer,
including starting the RPC server for handling requests related to volume
operations.

The module also sets up the logging and protocol configurations.

Entry Point:
    This module should be run as the main module to start the RPC server.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.volume.config import SERVICE_LAYER_DOMAIN_QUEUE_NAME
from intakevms.modules.volume.domain import model
from intakevms.libs.messaging.messaging_agents import MessagingServer

LOG = get_logger('domain-manager')


if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    server = MessagingServer(
        queue_name=SERVICE_LAYER_DOMAIN_QUEUE_NAME,
        manager=model.VolumeFactory(),
    )
    server.start()
