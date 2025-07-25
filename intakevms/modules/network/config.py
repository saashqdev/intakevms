from intakevms.config import RPC_QUEUES, data, get_default_session_factory

API_SERVICE_LAYER_QUEUE_NAME: str = RPC_QUEUES.Network.SERVICE_LAYER
SERVICE_LAYER_DOMAIN_QUEUE_NAME: str = RPC_QUEUES.Network.DOMAIN_LAYER
NETPLAN_DIR = '/etc/netplan/'
TEMPLATES_PATH = '/opt/virtman/intakevms/intakevms/modules/network/domain/'

DEFAULT_SESSION_FACTORY = get_default_session_factory()

NETWORK_CONFIG_MANAGER = data.get('network', {}).get('config_manager', 'ovs')
