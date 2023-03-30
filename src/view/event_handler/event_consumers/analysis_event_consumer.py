from abc import ABC
from abc import abstractmethod

from src.controller.output_handling.event import AnalysisAdded
from src.controller.output_handling.event import AnalysisChanged
from src.controller.output_handling.event import AnalysisDeleted
from src.controller.output_handling.event import AnalysisImported
from src.controller.output_handling.event import AnalysisRefreshed


class AnalysisEventConsumer(ABC):
    """
    An Interface that needs to be implemented by each class that should be able to process
    analysis events. The implementations of the interface functions can be very different so
    the documentation is found in the implementation of classes that implement this interface.
    """

    @abstractmethod
    def process_added_analysis(self, event: AnalysisAdded):
        """
        called whenever an AnalysisAdded event was thrown
        """
        pass

    @abstractmethod
    def process_imported_analysis(self, event: AnalysisImported):
        """
        called whenever an AnalysisImported event was thrown
        """
        pass

    @abstractmethod
    def process_deleted_analysis(self, event: AnalysisDeleted):
        """
        called whenever an AnalysisDeleted event was thrown
        """
        pass

    @abstractmethod
    def process_refreshed_analysis(self, event: AnalysisRefreshed):
        """
        called whenever an AnalysisRefreshed event was thrown
        """
        pass

    @abstractmethod
    def process_changed_analysis(self, event: AnalysisChanged):
        """
        called whenever an AnalysisChanged event was thrown
        """
        pass
