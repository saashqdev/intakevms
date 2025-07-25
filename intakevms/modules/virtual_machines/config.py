from intakevms import config
from intakevms.config import RPC_QUEUES, get_default_session_factory

API_SERVICE_LAYER_QUEUE_NAME: str = RPC_QUEUES.VMS.SERVICE_LAYER
SERVICE_LAYER_DOMAIN_QUEUE_NAME: str = RPC_QUEUES.VMS.DOMAIN_LAYER
VM_DRIVER = 'qemu-driver'
TEMPLATES_PATH = (
    '/opt/virtman/intakevms/intakevms/modules/virtual_machines/domain/templates/'
)
SNAPSHOTS_PATH = (
    '/opt/virtman/intakevms/data/snapshots/'
)
SERVER_IP = config.data.get('web_app', {}).get('host', 'localhost')

DEFAULT_SESSION_FACTORY = get_default_session_factory()