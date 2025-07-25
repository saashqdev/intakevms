"""Main entry point for the Block Device Service Layer Manager.

This module is responsible for starting the necessary components for the
Block Device Service Layer, including the ORM mappers, the RPCServer, and the
BlockDevicesServiceLayerManager service.

The script is designed to be the main entry point for the service layer
functionality, and it sets up the required infrastructure to handle block
device-related operations.

When executed as the main script, it performs the following actions:
1. Starts the ORM mappers for the block device and event store modules.
2. Starts the RPCServer to consume messages from the API Service Layer queue.
3. Initializes and starts the BlockDevicesServiceLayerManager service.

The BlockDevicesServiceLayerManager service is responsible for handling the
business logic and coordination of block device-related operations.
"""

from intakevms.libs.log import get_logger
from intakevms.modules.block_device.config import API_SERVICE_LAYER_QUEUE_NAME
from intakevms.libs.messaging.messaging_agents import MessagingServer
from intakevms.modules.block_device.service_layer import services

LOG = get_logger('service-layer-manager')


if __name__ == '__main__':
    """Main entry point for the Block Device Service Layer Manager."""
    LOG.info('Starting RPCServer for consuming')
    service = services.BlockDevicesServiceLayerManager
    service.start(block=False)
    server = MessagingServer(
        queue_name=API_SERVICE_LAYER_QUEUE_NAME,
        manager=service,
    )
    server.start()
