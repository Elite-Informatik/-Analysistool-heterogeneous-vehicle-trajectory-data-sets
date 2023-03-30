from typing import List

from src.controller.controller import IController
from src.model.analysis_structure.analysis_structure import AnalysisStructure
from src.model.facade_consumer.data_request_consumer import DataRequestConsumer
from src.model.filter_structure.filter_structure import FilterStructure
from src.model.imodel import IModel
from src.model.model_facade import ModelFacade
from src.model.polygon_structure.polygon_structure import PolygonStructure
from src.model.setting_structure.setting_structure import SettingStructure


class Model(IModel):
    """
    A concrete implementation of the IModel interface that represents a model in the system.
    """

    _model_facade: ModelFacade
    _request_consumer_list: List[DataRequestConsumer]

    def __init__(self):
        """
        Constructs a new Model object by initializing the required components and setting the underlying structures.
        """
        self._model_facade = ModelFacade()
        self._request_consumer_list = list()
        self.init_components()

    def init_components(self):
        """
        Initializes the required components for the model and sets the underlying structures.
        """
        # Connect polygon and filter
        polygon_structure: PolygonStructure = PolygonStructure()
        filter_structure: FilterStructure = FilterStructure(polygon_structure)
        polygon_structure.set_filter_facade(filter_structure)

        # setting structure
        setting_structure: SettingStructure = SettingStructure()

        # set analysis structure
        analysis_structure: AnalysisStructure = AnalysisStructure()
        self._request_consumer_list.append(analysis_structure)
        analysis_structure.set_polygon_structure(polygon_structure)

        self._model_facade.set_polygon_structure(polygon_structure)
        self._model_facade.set_filter_structure(filter_structure)
        self._model_facade.set_setting_structure(setting_structure)
        self._model_facade.set_analysis_structure(analysis_structure)
        """
        Sets the underlying structures for the ModelFacade object.
        """

    def set_controller(self, controller: IController):
        """
        Sets the controller used by the model, which will be used to pass data requests to the data request consumers
        in the request consumer list.
        :param controller: The IController object to set as the controller for the model.
        """
        for request_consumer in self._request_consumer_list:
            request_consumer.set_data_request(controller.data_request_facade)

    @property
    def model_facade(self) -> ModelFacade:
        return self._model_facade
