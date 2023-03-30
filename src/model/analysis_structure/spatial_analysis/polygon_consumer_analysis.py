from abc import ABC

from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


class PolygonFacadeConsumer(ABC):
    """
    A consumer for the polygon facade to the analyses that need it.
    """

    def set_polygon_structure(self, structure: IPolygonStructure):
        """
        Setter for the polygon structure
        """
        raise NotImplementedError
