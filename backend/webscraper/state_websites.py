import typing
from typing import Optional
from bs4 import BeautifulSoup
from abc import abstractmethod

import urllib3

http = urllib3.PoolManager(cert_reqs="CERT_NONE") # TODO: fix SSL certifications
urllib3.disable_warnings()


# query
class Query:
    def __init__(self, first_name: str, last_name: str, inmate_id: str, prison_name: str, add1: str, city: str, state: str, zip: str):
        self.data = {"first_name": first_name, "last_name": last_name, "inmate_id": inmate_id, "prison_name": prison_name,
            "add1": add1, "city": city, "state": state, "zip": zip}


# response
class Response:
    # simple check to see if two addresses match
    def address_match(self, add1, add2) -> bool:
        add1 = add1.strip().lower()
        add2 = add2.strip().lower()
        if add1 == "" or add2 == "":
            return add1 == add2 == ""
        return add1 == add2 or add1 in add2 or add2 in add1

    # constructor
    def __init__(self, prison_name: str, prison_address: str, old_prison_address: str):
        self.address_changed = not self.address_match(prison_address, old_prison_address)
        self.prison_name = prison_name
        self.prison_address = prison_address

    # to_string method for debugging
    def __str__(self):
        return f"Response(address_changed: {self.address_changed}, prison_name: {self.prison_name}, prison_address: {self.prison_address})"


# handles queries to a specific state website
class StateWebsite(object):
    # constructor
    def __init__(self, url, post_ext: str, input_map: dict[str, type: str]):
        self.url = url
        self.post_ext = post_ext
        self.input_map = input_map

    # visits base website
    def get_page(self) -> Optional[str]:
        resp = http.request('GET', self.url)
        if resp.status != 200:
            return None
        return resp.data if resp.status == 200 else None

    # inputs data into website and submits, landing on response page
    # can be overridden if needed
    def query_post(self, query: Query) -> Optional[BeautifulSoup]:
        # input fields
        fields = {}
        for name in query.data.keys():
            if name in self.input_map.keys():
                fields[self.input_map[name]] = query.data[name]

        # post
        post_resp = http.request('POST', self.url + "/" + self.post_ext, fields=fields)
        return BeautifulSoup(post_resp.data, "html.parser") if post_resp.status == 200 else None

    # handles full query + parsing response
    # should call query_post first to get response landing page
    @abstractmethod
    def query(self, query: Query):
        pass

# texas state website
class TexasWebsite(StateWebsite):
    def __init__(self):
        super().__init__("https://inmate.tdcj.texas.gov/InmateSearch/search.action", "search", {
            "first_name": "firstName",
            "last_name": "lastName"
        })

        # fetch unit address data page
        print("FETCHING TEXAS UNIT ADDRESSES")
        unit_addresses_url = 'https://www.tdcj.texas.gov/unit_directory/unit_information.html'
        resp = http.request('GET', unit_addresses_url)
        if resp.status != 200:
            raise Exception("Unit addresses website could not be loaded at url", unit_addresses_url)
        
        # scrape unit address data page to construct a unit -> address map
        soup = BeautifulSoup(resp.data, "html.parser")
        table = soup.find("table", {"class": "tdcj_table", "summary": "The following table lists each unit, address, and telephone number"})
        rows = table.find_all("tr")
        self.unit_address: dict[str, type: str] = {}
        for row in rows:
            data = row.find_all("td")
            if len(data) != 3:
                continue
            self.unit_address[data[0].text.strip().lower()] = data[1].text.strip()
        print(self.unit_address)

    # overrides query in parent class
    def query(self, query: Query) -> list[type: Response]:
        # get landing page of query
        landing_page = super().query_post(query)
        if landing_page is None:
            return []

        # scrape data from landing page
        table = landing_page.find("table", {"class": "tdcj_table"})
        if table is None:
            return []
        rows = table.find_all("tr")
        results = []
        for row in rows:
            row_data = row.find_all("td")
            if len(row_data) < 6:
                continue
            unit = row_data[5].text.strip().lower()
            address = self.unit_address[unit] if unit in self.unit_address.keys() else f"UNIT: {unit} (unknown address)"
            results.append(Response(f"{unit.upper()} UNIT", address, query.data["add1"]))

        return results


# maps state id to state website
state_websites = {
    "AL": None,                     # Alabama
    "AK": None,                     # Alaska
    "AZ": None,                     # Arizona
    "AR": None,                     # Arkansas
    "CA": None,                     # California
    "CO": None,                     # Colorado
    "CT": None,                     # Connecticut
    "DE": None,                     # Delaware
    "DC": None,                     # District of Columbia
    "FL": None,                     # Florida
    "GA": None,                     # Georgia
    "HI": None,                     # Hawaii
    "ID": None,                     # Idaho
    "IL": None,                     # Illinois
    "IN": None,                     # Indiana
    "IA": None,                     # Iowa
    "KS": None,                     # Kansas
    "KY": None,                     # Kentucky
    "LA": None,                     # Louisiana
    "ME": None,                     # Maine
    "MD": None,                     # Maryland
    "MA": None,                     # Massachusetts
    "MI": None,                     # Michigan
    "MN": None,                     # Minnesota
    "MS": None,                     # Mississippi
    "MO": None,                     # Missouri
    "MT": None,                     # Montana
    "NE": None,                     # Nebraska
    "NV": None,                     # Nevada
    "NH": None,                     # New Hampshire
    "NJ": None,                     # New Jersey
    "NM": None,                     # New Mexico
    "NY": None,                     # New York
    "NC": None,                     # North Carolina
    "ND": None,                     # North Dakota
    "OH": None,                     # Ohio
    "OK": None,                     # Oklahoma
    "OR": None,                     # Oregon
    "PA": None,                     # Pennsylvania
    "RI": None,                     # Rhode Island
    "SC": None,                     # South Carolina
    "SD": None,                     # South Dakota
    "TN": None,                     # Tennessee
    "TX": TexasWebsite(),           # Texas
    "UT": None,                     # Utah
    "VT": None,                     # Vermont
    "VA": None,                     # Virginia
    "WA": None,                     # Washington
    "WV": None,                     # West Virginia
    "WI": None,                     # Wisconsin
    "WY": None,                     # Wyoming
}