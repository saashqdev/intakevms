"""Service layer manager for event processing.

This module defines the EventstoreServiceLayerManager, which handles
service-level operations such as database transactions and messaging.

Classes:
    - EventstoreServiceLayerManager: Manager handling event service logic.

Dependencies:
    - MessagingClient: Handles message-based communication.
    - EventstoreSqlAlchemyUnitOfWork: Unit of Work for event operations.
"""

from typing import Dict, List

from intakevms.libs.log import get_logger
from intakevms.modules.base_manager import BackgroundTasks
from intakevms.modules.event_store.config import API_SERVICE_LAYER_QUEUE_NAME
from intakevms.libs.messaging.messaging_agents import MessagingClient
from intakevms.modules.event_store.service_layer import unit_of_work2
from intakevms.modules.event_store.adapters.serializer import DataSerializer

LOG = get_logger(__name__)


class EventstoreServiceLayerManager(BackgroundTasks):
   """Manager for coordinating event operations in the service layer.

   This class orchestrates event-related tasks such as creation and
   get operations. It handles RPC communication and database transactions.

   Attributes:
      uow (EventstoreSqlAlchemyUnitOfWork): Unit of Work for event
         transactions.
      service_layer_rpc (MessagingClient): RPC client for internal task
         delegation.
   """

   def __init__(self) -> None:
      """Initialize the EventstoreServiceLayerManager.

      Sets up messaging client and unit of work.
      """
      super().__init__()
      self.uow = unit_of_work2.EventstoreSqlAlchemyUnitOfWork
      self.service_layer_rpc = MessagingClient(
            queue_name=API_SERVICE_LAYER_QUEUE_NAME
      )

   def get_all_events(self) -> List:
      """Retrieve all events from the database.

      Returns:
         List: A list of serialized event representations.
      """
      LOG.info('Getting events, service layer')
      with self.uow() as uow:
         return [
            DataSerializer.to_web(event)
            for event in uow.events.get_all()
         ]

   def get_all_events_by_module(self, data: Dict) -> List:
      """Retrieve all events by module from the database.

      Returns:
         List: A list of serialized event representations.
      """
      LOG.info(f'Getting events by module {data["module_name"]}, service layer')
      with self.uow() as uow:
         return [
            DataSerializer.to_web(event)
            for event in uow.events.get_all_by_module(data['module_name'])
         ]

   def get_last_events(self, data: Dict) -> List:
      """Retrieve a certain number of last events from the database.

      Returns:
         List: A list of serialized event representations.
      """
      LOG.info('Getting last events, service layer')
      with self.uow() as uow:
         return [
            DataSerializer.to_web(event)
            for event in uow.events.get_last_events(data['limit'])
         ]

   def add_event(self, data: Dict) -> None:
      """Create a new event, persist it in the db, start async creation.

      Args:
         data (Dict): A dictionary with event creation fields.

      Returns:
         None
      """
      LOG.info('Adding event, service layer')
      with self.uow() as uow:
         db_event = DataSerializer.to_db(data)
         uow.events.add(db_event)
         uow.commit()