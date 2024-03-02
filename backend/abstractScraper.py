from abc import ABC, abstractmethod
from query import Query, PrisonMatch


class AbstractStateScraper(ABC):
    """
    This should initialize the scraper, loading data from a cache if possible and asked for
    Once the scraper is initialized, data should be cached if asked for
    """
    def load(self, use_cache=True) -> None:
        pass

    @abstractmethod
    def query(self, query: Query) -> list[type: PrisonMatch]:
        pass

