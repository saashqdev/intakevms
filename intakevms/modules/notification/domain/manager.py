"""Domain manager for handling notification consumption.

This module starts the RPC server that consumes notifications and delegates
them to the appropriate handlers.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.notification.config import SERVICE_LAYER_DOMAIN_QUEUE_NAME
from intakevms.modules.notification.domain import model
from intakevms.libs.messaging.messaging_agents import MessagingServer

LOG = get_logger('domain-manager')

if __name__ == '__main__':
    LOG.info('Starting RPCServer for consuming')
    server = MessagingServer(
        queue_name=SERVICE_LAYER_DOMAIN_QUEUE_NAME,
        manager=model.NotificationFactory(),
    )
    server.start()
