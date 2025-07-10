from sqlalchemy.orm import sessionmaker

from intakevms.config import get_default_session_factory

DEFAULT_SESSION_FACTORY: sessionmaker = get_default_session_factory()
