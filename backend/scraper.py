from query import Query

from states import NewYork, Texas, Pennsylvania
from states import NorthCarolina
from abstractScraper import AbstractStateScraper
from threading import Thread
import urllib3
urllib3.disable_warnings()

class Scraper:
    def __init__(self) -> None:
        self.state_websites : dict[str, AbstractStateScraper] = {
            "NY": NewYork.NewYorkScraper(),
            "TX": Texas.TexasScraper(),
            "PA": Pennsylvania.PennsylvaniaScraper(),
            "NC": NorthCarolina.NorthCarolinaScraper(),
        }

        constructors : list[type: Thread]= []

        for value in self.state_websites.values():
            thread = Thread(target=value.load)
            thread.start()
            constructors.append(thread)
        
        for thread in constructors:
            thread.join()
        
        print("scraper ready")

    def add_scraper(self, state: str, constructor)-> None:
        self.state_websites[state] = constructor()

    def query(self, query: Query):
        state_scraper = self.state_websites.get(query["state"])
        if state_scraper == None:
            return []
        else:
            return state_scraper.query(query)