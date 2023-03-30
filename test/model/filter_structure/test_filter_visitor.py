from unittest import TestCase
from uuid import uuid4

from src.data_transfer.content import Column
from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord
from src.model.filter_structure.composite.filter_group import FilterGroup
from src.model.filter_structure.composite.filters.discrete_filter import DiscreteFilter
from src.model.filter_structure.composite.filters.interval_filter import IntervalFilter
from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
from src.model.filter_structure.filter_factory import FilterFactory
from src.model.filter_structure.filter_handler import FilterHandler
from src.model.filter_structure.point_filter_visitor import PointFilterVisitor
from src.model.polygon_structure.polygon_structure import PolygonStructure


class TestPointFilterVisitor(TestCase):
    def setUp(self):
        self.filter_visitor = PointFilterVisitor()

    def test_create_string(self):
        polygon_structure = PolygonStructure()
        filter_factory = FilterFactory(polygon_structure)
        filter_structure = FilterHandler(filter_factory.create_group(
            FilterGroupRecord("aal123", "löl", True, False, (), "AND"))
            , 'löl')
        uuid_polygon1 = polygon_structure.add_polygon(
            PolygonRecord((PositionRecord(0, 0), PositionRecord(1, 0), PositionRecord(0, 1)), "poly das polygon"))
        uuid_poygon2 = polygon_structure.add_polygon(
            PolygonRecord((PositionRecord(1, 1), PositionRecord(2, 1), PositionRecord(1, 2)), "poly das polygon"))
        filter_structure.add(PolygonFilter(uuid4(), "a", polygon_structure, [uuid_polygon1]),
                             filter_structure.get_root_id())
        filter_structure.accept_visitor(self.filter_visitor)
        self.assertEqual(
            "((ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude))))",
            self.filter_visitor.get_sql_request())
        self.klammertest()

        filter_structure.add(IntervalFilter(uuid4(), "b", Column.SPEED, 25, 39), filter_structure.get_root_id())
        self.assertEqual(
            "((ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude))))",
            self.filter_visitor.get_sql_request())
        self.klammertest()

    def test_create_string_2(self):
        polygon_structure = PolygonStructure()
        filter_factory = FilterFactory(polygon_structure)
        filter_structure = FilterHandler(filter_factory.create_group(
            FilterGroupRecord("aal123", "lol", True, False, (), "AND")), 'lol')
        uuid_polygon1 = polygon_structure.add_polygon(
            PolygonRecord((PositionRecord(0, 0), PositionRecord(1, 0), PositionRecord(0, 1)), "poly das polygon"))
        uuid_poygon2 = polygon_structure.add_polygon(
            PolygonRecord((PositionRecord(1, 1), PositionRecord(2, 1), PositionRecord(1, 2)), "poly das polygon"))
        filter_structure.add(PolygonFilter(uuid4(), "a", polygon_structure, [uuid_polygon1]),
                             filter_structure.get_root_id())
        filter_structure.add(IntervalFilter(uuid4(), "b", Column.SPEED, 25, 39), filter_structure.get_root_id())
        filter_structure.accept_visitor(self.filter_visitor)
        self.assertEqual(
            "((ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude))) and (speed between 25 and 39))",
            self.filter_visitor.get_sql_request())
        self.klammertest()

        uuid_group1 = uuid4()
        filter_structure.add(FilterGroup(LogicalOperator.OR, uuid_group1, "gruppe"), filter_structure.get_root_id())
        self.filter_visitor = PointFilterVisitor()
        filter_structure.accept_visitor(self.filter_visitor)
        self.assertEqual(
            "((ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude))) and (speed between 25 and 39))",
            self.filter_visitor.get_sql_request())
        self.klammertest()

        filter_structure.add(DiscreteFilter(uuid4(), "diskret", Column.ONE_WAY_STREET, ["false"]), uuid_group1)
        self.filter_visitor = PointFilterVisitor()
        filter_structure.accept_visitor(self.filter_visitor)
        self.assertEqual(
            "((ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude))) and (speed between 25 and 39) and ((one_way_street in ('false'))))",
            self.filter_visitor.get_sql_request())
        self.klammertest()

        filter_structure.add(PolygonFilter(uuid4(), "ja", polygon_structure, [uuid_polygon1, uuid_poygon2]),
                             uuid_group1)
        self.filter_visitor = PointFilterVisitor()
        filter_structure.accept_visitor(self.filter_visitor)
        self.assertEqual(
            "((ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude))) and (speed between 25 and 39) and ((one_way_street in ('false')) or (ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(0 0, 1 0, 0 1, 0 0)')), ST_POINT(latitude, longitude)) and ST_Contains(ST_MakePolygon(ST_GeomFromText('LINESTRING(1 1, 2 1, 1 2, 1 1)')), ST_POINT(latitude, longitude)))))",
            self.filter_visitor.get_sql_request())
        self.klammertest()

    def klammertest(self):
        klammerausdruck = self.filter_visitor.get_sql_request()
        i = 0
        for a in klammerausdruck:
            if a == "(":
                i += 1
            if a == ")":
                i -= 1
        self.assertEqual(i, 0, "Klammeranzahl stimmt nicht")


class TestLogicalOperator(TestCase):
    def test_and(self):
        string1 = "apple"
        string2 = "bürne"
        self.assertEqual(LogicalOperator.AND.join_requests([string1, string2]), "(" + string1 + " and " + string2 + ")")

    def test_or(self):
        string1 = "apple"
        string2 = "bürne"
        self.assertEqual(LogicalOperator.OR.join_requests([string1, string2]), "(" + string1 + " or " + string2 + ")")
