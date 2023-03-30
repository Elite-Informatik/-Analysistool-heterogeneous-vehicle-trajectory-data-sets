import unittest

from src.data_transfer.record.settings_record import PageRecord
from src.model.setting_structure.page import Page
from src.model.setting_structure.segment import Segment
from src.model.setting_structure.setting import Setting


class TestPage(unittest.TestCase):
    def setUp(self) -> None:
        self.segments = [Segment(name="Segment 1", settings=[], identifier=""),
                         Segment(name="Segment 2", settings=[], identifier="")]
        self.page = Page(name="Page 1", segments=self.segments, identifier="")

    def test_add_segment(self):
        """Test that a segment can be added to the page and the count of segments increases by 1"""
        initial_count = len(self.page.get_segments())
        self.assertTrue(self.page.add_segment(Segment(name="Segment 3", settings=[], identifier="")))
        self.assertEqual(len(self.page.get_segments()), initial_count + 1)
        self.assertFalse(self.page.add_segment(self.segments[0]))
        self.assertEqual(len(self.page.get_segments()), initial_count + 1)

    def test_get_segments(self):
        """Test that the correct segments are returned by the get_segments method"""
        self.assertEqual(self.page.get_segments(), self.segments)

    def test_get_name(self):
        """Test that the correct _name is returned by the get_name method"""
        self.assertEqual(self.page.get_name(), "Page 1")

    def test_get_record(self):
        segments = [Segment("", "Segment 1", [Setting.from_list(identifier="", name="Setting 1",
                                                                option_list=[1, 2, 3], standard=2, ),
                                              Setting.from_interval(identifier="", name="Setting 2", minimum=1,
                                                                    maximum=10,
                                                                    standard=5, )]),
                    Segment("", "Segment 2", [Setting.from_string(identifier="", regex="[a-z]+", standard="hello",
                                                                  name="Setting 3")])]
        page = Page("", "Page 1", segments)
        page_record = page.get_record()
        self.assertIsInstance(page_record, PageRecord)
        self.assertEqual(page_record.name, "Page 1")
        self.assertEqual(page_record.segment_records[0]._name, "Segment 1")
        self.assertEqual(page_record.page_tuple[1][0].segment[1][0].context, "Setting 1")
        self.assertEqual(page_record.page_tuple[1][0].segment[1][1].context, "Setting 2")
        self.assertEqual(page_record.page_tuple[1][1].segment[0], "Segment 2")
        self.assertEqual(page_record.page_tuple[1][1].segment[1][0].context, "Setting 3")


if __name__ == '__main__':
    unittest.main()
