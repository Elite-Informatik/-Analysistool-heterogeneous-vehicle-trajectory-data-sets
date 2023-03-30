import unittest
from uuid import uuid4

from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened
from src.view.event_handler import EventHandler
from src.view.event_handler.event_consumers import DatasetEventConsumer


class TestDatasetEventConsumer(DatasetEventConsumer):
    def __init__(self):
        self.added = None
        self.deleted = None
        self.opened = None

    def process_added_dataset(self, event: DatasetAdded):
        self.added = event.id

    def process_deleted_dataset(self, event: DatasetDeleted):
        self.deleted = event.id

    def process_opened_dataset(self, event: DatasetOpened):
        self.opened = event


class TestEventHandlerDatasetEvents(unittest.TestCase):

    def initialize_event_handler(self):
        self._event_handler = EventHandler()

    def test_dataset_events(self):
        pass
        self.initialize_event_handler()

        # create and subscribe consumers
        dataset_consumer1 = TestDatasetEventConsumer()
        dataset_consumer2 = TestDatasetEventConsumer()
        self._event_handler.subscribe_dataset_events(dataset_consumer1)
        self._event_handler.subscribe_dataset_events(dataset_consumer2)

        # create dataset events
        dataset_added = DatasetAdded(_id=uuid4())
        dataset_deleted = DatasetDeleted(_id=uuid4())
        dataset_opened = DatasetOpened()

        # send events to events handler
        self._event_handler.notify_event(dataset_added)
        self._event_handler.notify_event(dataset_deleted)
        self._event_handler.notify_event(dataset_opened)

        # proof if the events have reached the consumers
        self.assertTrue(dataset_consumer1.added == dataset_added.id)
        self.assertTrue(dataset_consumer1.deleted == dataset_deleted.id)
        self.assertTrue(dataset_consumer1.opened is dataset_opened)

        self.assertTrue(dataset_consumer2.added == dataset_added.id)
        self.assertTrue(dataset_consumer2.deleted == dataset_deleted.id)
        self.assertTrue(dataset_consumer2.opened is dataset_opened)

        # unsubscribe the first consumer
        self._event_handler.unsubscribe_dataset_events(dataset_consumer1)

        # initialize new events (dataset_opened1 is new variable to create new instance.
        # Otherwise the instance would be the same)
        dataset_added = DatasetAdded(_id=uuid4())
        dataset_deleted = DatasetDeleted(_id=uuid4())
        dataset_opened1 = DatasetOpened()

        # send new events to the events handler
        self._event_handler.notify_event(dataset_added)
        self._event_handler.notify_event(dataset_deleted)
        self._event_handler.notify_event(dataset_opened1)

        # proof that only the second consumer got the events
        self.assertFalse(dataset_consumer1.added == dataset_added.id)
        self.assertFalse(dataset_consumer1.deleted == dataset_deleted.id)
        self.assertFalse(dataset_consumer1.opened is dataset_opened1)

        self.assertTrue(dataset_consumer2.added == dataset_added.id)
        self.assertTrue(dataset_consumer2.deleted == dataset_deleted.id)
        self.assertTrue(dataset_consumer2.opened is dataset_opened1)
