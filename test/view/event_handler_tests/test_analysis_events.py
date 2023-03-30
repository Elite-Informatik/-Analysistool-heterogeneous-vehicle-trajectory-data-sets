import unittest
from uuid import uuid4

from src.controller.output_handling.event import AnalysisAdded
from src.controller.output_handling.event import AnalysisChanged
from src.controller.output_handling.event import AnalysisDeleted
from src.controller.output_handling.event import AnalysisImported
from src.controller.output_handling.event import AnalysisRefreshed
from src.view.event_handler import EventHandler
from src.view.event_handler.event_consumers import AnalysisEventConsumer


class Tes_tAnalysisEventConsumer(AnalysisEventConsumer):

    def __init__(self):
        self.AddedAnalysis: AnalysisAdded = None
        self.DeletedAnalysis: AnalysisDeleted = None
        self.RefreshedAnalysis: AnalysisRefreshed = None

    def process_added_analysis(self, event: AnalysisAdded):
        self.AddedAnalysis = event.id

    def process_deleted_analysis(self, event: AnalysisDeleted):
        self.DeletedAnalysis = event.id

    def process_refreshed_analysis(self, event: AnalysisRefreshed):
        self.RefreshedAnalysis = event.id

    def process_changed_analysis(self, event: AnalysisChanged):
        self.RefreshedAnalysis = event.id

    def process_imported_analysis(self, event: AnalysisImported):
        pass


class TestEventHandlerAnalysisEvents(unittest.TestCase):

    def initialize_event_handler(self):
        self._event_handler = EventHandler()

    def test_analysis_events(self):
        self.initialize_event_handler()

        # create and subscribe events consumers
        analysis_consumer1 = Tes_tAnalysisEventConsumer()
        analysis_consumer2 = Tes_tAnalysisEventConsumer()
        self._event_handler.subscribe_analysis_events(analysis_consumer1)
        self._event_handler.subscribe_analysis_events(analysis_consumer2)

        # create example events
        analysis_added = AnalysisAdded(_id=uuid4())
        analysis_deleted = AnalysisDeleted(_id=uuid4())
        analysis_refreshed = AnalysisRefreshed(_id=uuid4())

        # send events to events handler
        self._event_handler.notify_event(analysis_added)
        self._event_handler.notify_event(analysis_deleted)
        self._event_handler.notify_event(analysis_refreshed)

        # proof that the events have reached the consumers
        self.assertTrue(analysis_consumer1.RefreshedAnalysis == analysis_refreshed.id)
        self.assertTrue(analysis_consumer1.AddedAnalysis == analysis_added.id)
        self.assertTrue(analysis_consumer1.DeletedAnalysis == analysis_deleted.id)

        self.assertTrue(analysis_consumer2.RefreshedAnalysis == analysis_refreshed.id)
        self.assertTrue(analysis_consumer2.DeletedAnalysis == analysis_deleted.id)
        self.assertTrue(analysis_consumer2.AddedAnalysis == analysis_added.id)

        # unsubscribe the first consumer
        self._event_handler.unsubscribe_analysis_events(analysis_consumer1)

        # create new example events
        analysis_added = AnalysisAdded(_id=uuid4())
        analysis_deleted = AnalysisDeleted(_id=uuid4())
        analysis_refreshed = AnalysisRefreshed(_id=uuid4())

        # send example events
        self._event_handler.notify_event(analysis_added)
        self._event_handler.notify_event(analysis_deleted)
        self._event_handler.notify_event(analysis_refreshed)

        # proof that only the second consumer got the events
        self.assertFalse(analysis_consumer1.AddedAnalysis == analysis_added.id)
        self.assertFalse(analysis_consumer1.DeletedAnalysis == analysis_deleted.id)
        self.assertFalse(analysis_consumer1.RefreshedAnalysis == analysis_refreshed.id)

        self.assertTrue(analysis_consumer2.AddedAnalysis == analysis_added.id)
        self.assertTrue(analysis_consumer2.RefreshedAnalysis == analysis_refreshed.id)
        self.assertTrue(analysis_consumer2.DeletedAnalysis == analysis_deleted.id)
