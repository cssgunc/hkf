from typing import Optional
from bs4 import BeautifulSoup

from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper
import json
import os
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
}


# texas state website
class TexasScraper(AbstractStateScraper):
    def load(self, use_cache=True):
        print("initializing texas")
        file_path = "stateCache/Texas.json"
        if use_cache and os.path.exists(file_path):  # Check if the file exists
            with open(file_path, "r") as file:
                self.unit_address = json.load(file)  # Load data from the JSON file
            print("initialized texas from cache")
        else:
            print("initializing texas from web")
            unit_addresses_url = (
                "https://www.tdcj.texas.gov/unit_directory/unit_information.html"
            )
            resp = requests.get(unit_addresses_url, headers=headers, verify=False)
            if resp.status_code != 200:
                raise Exception(
                    "Unit addresses website could not be loaded at url",
                    unit_addresses_url,
                )

            # scrape unit address data page to construct a unit -> address map
            soup = BeautifulSoup(resp.text, "html.parser")
            table = soup.find(
                "table",
                {
                    "class": "tdcj_table",
                    "summary": "The following table lists each unit, address, and telephone number",
                },
            )
            rows = table.find_all("tr")
            self.unit_address: dict[str, type:str] = {}
            for row in rows:
                data = row.find_all("td")
                if len(data) != 3:
                    continue
                self.unit_address[data[0].text.strip().lower()] = data[1].text.strip()
            print("initialized texas from web")
            if use_cache:
                with open(file_path, "w") as file:
                    json.dump(
                        self.unit_address, file, indent=4
                    )  # Cache data to file_path

    def query_post(self, query: Query) -> Optional[BeautifulSoup]:
        url = "https://inmate.tdcj.texas.gov/InmateSearch/search.action"
        post_ext = "search"
        fields = {"firstName": query["first_name"], "lastName": query["last_name"]}

        post_resp = requests.post(url + "/" + post_ext, data=fields, headers=headers, verify=False)
        return (
            BeautifulSoup(post_resp.text, "html.parser")
            if post_resp.status_code == 200
            else None
        )

    # overrides query in parent class
    def query(self, query: Query) -> list[type:PrisonMatch]:
        # get landing page of query
        landing_page = self.query_post(query)
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
            address = (
                self.unit_address[unit]
                if unit in self.unit_address.keys()
                else f"UNIT: {unit} (unknown address)"
            )
            results.append(PrisonMatch.create(f"{unit.upper()} UNIT", address, query["add1"]))
        return results
