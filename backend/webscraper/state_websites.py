import typing
from bs4 import BeautifulSoup
from abc import abstractmethod

import urllib3

http = urllib3.PoolManager()


# handles queries to a specific state website
class StateWebsite(object):
    def __init__(self, url, post_ext: str, input_map: dict[str, type: str]):
        self.url = url
        self.post_ext = post_ext
        self.input_map = input_map

    # visits base website
    def get_page(self) -> str | None:
        resp = http.request('GET', self.url)
        if resp.status != 200:
            return None
        return resp.data if resp.status == 200 else None

    # inputs data into website and submits, landing on response page
    # can be overridden if needed
    def query_post(self, data: dict[str, type: str]) -> BeautifulSoup | None:
        # input fields
        fields = {}
        for name in data.keys():
            if name in self.input_map.keys():
                fields[self.input_map[name]] = data[name]

        # post
        post_resp = http.request('POST', self.url + "/" + self.post_ext, fields=fields)
        return BeautifulSoup(post_resp.data, "html.parser") if post_resp.status == 200 else None

    # handles full query + parsing response
    # should call query_post first to get response landing page
    @abstractmethod
    def query(self, data: dict[str, type: str]):
        pass


class TexasWebsite(StateWebsite):
    def __init__(self):
        super().__init__("https://inmate.tdcj.texas.gov/InmateSearch/search.action", "search", {
            "first_name": "firstName",
            "last_name": "lastName"
        })

    def query(self, data: dict[str, type: str]) -> dict | None:
        landing_page = super().query_post(data)
        # TODO: pull data from landing page
        return {"landing_page": landing_page} if landing_page is not None else None


# maps state id to state website
state_websites = {}
state_websites["TX"] = TexasWebsite()