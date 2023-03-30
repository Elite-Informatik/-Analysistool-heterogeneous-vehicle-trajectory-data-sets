from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4

from src.controller.output_handling.abstract_event import Event
from src.controller.output_handling.event import AnalysisAdded
from src.controller.output_handling.event import AnalysisDeleted
from src.controller.output_handling.event import AnalysisRefreshed
from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened
from src.controller.output_handling.event import FilterAdded
from src.controller.output_handling.event import FilterChanged
from src.controller.output_handling.event import FilterComponentDeleted
from src.controller.output_handling.event import FilterGroupAdded
from src.controller.output_handling.event import FilterGroupChanged
from src.controller.output_handling.event import FilterMovedToGroup
from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonChanged
from src.controller.output_handling.event import PolygonDeleted
from src.controller.output_handling.event import RefreshTrajectoryData
from src.controller.output_handling.event import SettingsChanged
from src.controller.output_handling.event_manager import EventManager
from src.view.event_handler import EventHandler

ABSTRACT = {Event}
EVENTS = {DatasetOpened, RefreshTrajectoryData, SettingsChanged}
ID_EVENTS = {AnalysisAdded, AnalysisRefreshed, AnalysisDeleted, DatasetAdded, DatasetDeleted, FilterChanged,
             FilterComponentDeleted, FilterGroupChanged, PolygonAdded, PolygonChanged, PolygonDeleted}
TWO_ID_EVENTS = {FilterAdded, FilterMovedToGroup, FilterGroupAdded}


class EventTest(TestCase):
    def test_events_subclass(self):
        for eventtype in ABSTRACT:
            try:
                self.assertRaises(TypeError, eventtype())
            except AssertionError:
                self.fail(f"Test failed: {eventtype} should raise TypeError when initialized")

        for eventtype in EVENTS:
            try:
                eventtype()
            except Exception as e:
                self.fail(f"Test failed: unexpected exception raised when initializing {eventtype}. {e}")

        event_lists = [EVENTS, ID_EVENTS, TWO_ID_EVENTS]
        for event_list in event_lists:
            for eventtype in event_list:
                try:
                    self.assertTrue(issubclass(eventtype, Event))
                except AssertionError:
                    self.fail(f"Test failed: {eventtype} is not a subclass of Event")

    def test_events_attributes(self):
        for eventtype in ID_EVENTS:
            uuid_1 = uuid4()
            event = eventtype(uuid_1)
            try:
                self.assertRaises(FrozenInstanceError, event.__setattr__, "id", uuid4())
            except AssertionError:
                self.fail(f"Test failed: {eventtype} should raise FrozenInstanceError when changing the 'id' attribute")
            try:
                self.assertTrue(uuid_1 == event.id)
            except AssertionError:
                self.fail(f"Test failes: {eventtype} doesen't save the id")

        for eventtype in TWO_ID_EVENTS:
            uuid_1 = uuid4()
            uuid_2 = uuid4()
            event = eventtype(uuid_1, uuid_2)
            try:
                self.assertRaises(FrozenInstanceError, event.__setattr__, "id", uuid4())
                self.assertRaises(FrozenInstanceError, event.__setattr__, "group_id", uuid4())
            except AssertionError:
                self.fail(
                    f"Test failed: {eventtype} should raise FrozenInstanceError when changing the 'id' or 'group_id' "
                    f"attribute")

            try:
                self.assertTrue(uuid_1 == event.id)
                self.assertTrue(uuid_2 == event.group_id)
            except AssertionError:
                self.fail(f"Test failes: {eventtype} doesen't save the 'id' or 'group_id' attribute")


class TestEventManager(TestCase):
    def test_event_manager_1(self):
        event_manager = EventManager()

        event_handler1 = EventHandler()
        event_handler2 = EventHandler()
        event_handler2.notify_event = MagicMock()
        event_handler1.notify_event = MagicMock()
        event_manager.subscribe(event_handler1)
        event1 = AnalysisAdded(uuid4())
        event_manager.notify(list([event1]))
        # event_handler1.notify_event.assert_called_once_with(event1)
        event_handler2.notify_event.assert_not_called()

        event_handler1.notify_event.reset_mock()
        event_manager.subscribe(event_handler2)
        event_manager.unsubscribe(event_handler1)
        event2 = DatasetOpened()
        event_manager.notify(list([event1, event2]))
        event_handler1.notify_event.assert_not_called()
        # event_handler2.notify_event.assert_has_calls([call(event1), call(event2)])

    def test_event_manager_2(self):
        # Test multiple subscription
        event_manager = EventManager()

        event_handler1 = EventHandler()
        event_handler2 = EventHandler()
        event_handler2.notify_event = MagicMock()
        event_handler1.notify_event = MagicMock()
        event_manager.subscribe(event_handler1)
        event_manager.subscribe(event_handler2)
        event1 = AnalysisAdded(uuid4())
        event_manager.notify(list([event1]))
        # event_handler1.notify_event.assert_called_once_with(event1)
        # event_handler2.notify_event.assert_called_once_with(event1)
