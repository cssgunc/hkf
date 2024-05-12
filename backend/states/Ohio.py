from bs4 import BeautifulSoup
import requests
from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper
import json
import os

state_api_url = "https://appgateway.drc.ohio.gov"
state_url = "https://drc.ohio.gov"
name_query_url = "/OffenderSearch/Search/SearchResults"

facilities_url = r"https://drc.ohio.gov/wps/wcm/connect/gov/Ohio%20Content%20English/odrc?source=library&srv=cmpnt&cmpntid=085753d2-876e-43ee-9d00-ed28ba0ac8bf&location=Ohio Content English//odrc/about/facilities&category="

def safeHeaders():
    return {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }



def fetch_name(firstname, lastname):
    data = {
        'FirstName': firstname,
        'LastName': lastname
    }

    response = requests.post(state_api_url + name_query_url, data=data, headers=safeHeaders())
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find_all(string="Your search only returned one record."):
        return [get_facility(soup)]

    links = soup.find_all('a', href=lambda href: href and href.startswith("/OffenderSearch/Search/Details/"))
    link_list = [link['href'] for link in links]

    def parse_link(link):
        response = requests.get(state_api_url + link, headers=safeHeaders())
        soup = BeautifulSoup(response.text, 'html.parser')
        return get_facility(soup)

    return map(parse_link, link_list)


def get_facility(soup: BeautifulSoup):
    institution_link = soup.find('a', string='Institution')

    if institution_link:
        next_neighbor_text = institution_link.parent.find_next_sibling().get_text(strip=True)
        return next_neighbor_text.removesuffix(" Correctional Institution")
    else:
        return None

def fetchFacilities():
    locationLinks = set()
    resp = requests.get(facilities_url, headers=safeHeaders())
    if resp.status_code != 200:
        raise Exception("location website could not be loaded at url", facilities_url)

    for entry in resp.json():
        locationLinks.add(entry['url'])



    facilityMap = {}
    for link in locationLinks:
        resp = requests.get(state_url+link, headers=safeHeaders())
        if resp.status_code != 200:
            print("ERROR")
            raise Exception("location website could not be loaded at url", state_url+link)
    
        soup = BeautifulSoup(resp.text, 'html.parser')

        name = link.removeprefix("/location/").removesuffix("-correctional-facility").lower()

        containers = soup.find_all(["strong","b"])

        found = False

        for container in containers:
            if container.get_text(strip=True).startswith("Address"):
                address = container.parent.get_text().removeprefix("Address:").strip().replace("\n", " ").replace(u'\xa0', u' ')
                name = link.split("/")[-1].strip().removesuffix("-correctional")

                facilityMap[name]=address
                found = True
                break
        if not found:
            print(link)
    return facilityMap

class OhioScraper(AbstractStateScraper):
    def load(self, use_cache = True):
        print("initializing ohio")
        file_path = "stateCache/Ohio.json"
        if use_cache and os.path.exists(file_path): # Check if the file exists
            with open(file_path, 'r') as file:
                self.facilityMap = json.load(file) # Load data from the JSON file
            print("initialized ohio from cache")
        else:
            print("initializing ohio from web")
            self.facilityMap = fetchFacilities() # Fetch data if file doesn't exist
            print("initialized ohio from web")
            if use_cache:
                with open(file_path, 'w') as file:
                    json.dump(self.facilityMap, file, indent=4) # Cache data to file_path
    def query(self, query: Query) -> list[type: PrisonMatch]:
        responses = []
        data = fetch_name(query["first_name"], query["last_name"])

        for match in data:
            if match==None:
                continue
            unit = match.lower()
            address = self.facilityMap[unit] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"

            responses.append(PrisonMatch.create(f"{unit.upper()} UNIT", address, query["add1"]))
        return responses