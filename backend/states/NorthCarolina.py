from bs4 import BeautifulSoup
import requests
import json
import os

from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper

facilities_url = "https://www.dac.nc.gov/divisions-and-sections/institutions/prison-facilities-regional-offices"
state_url = "https://www.dac.nc.gov"

def safeHeaders():
    return {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }

def fetch_name(firstname, lastname):
    data = {
        "searchFirstName":firstname,
        "searchLastName": lastname
    }

    response = requests.post("https://webapps.doc.state.nc.us/opi/offendersearch.do;jsessionid=8-C4H11Qh0ZlGB2kUbGti4vYeLRVAxRFC5T6VnL3.wv6jfhap97p_720?method=list", data=data, headers=safeHeaders())

    soup =  BeautifulSoup(response.text, 'html.parser')
    row = soup.find("a", string="Offender Number").parent.parent.findNextSibling()

    ids = []

    while row:
        ids.append(process_id(row.findChild().get_text(strip=True)))
        row = row.findNextSibling()
    return ids

def process_id(id):
    response = requests.get("https://webapps.doc.state.nc.us/opi/viewoffender.do?method=view&offenderID="+id, headers=safeHeaders())
    soup =  BeautifulSoup(response.text, 'html.parser')
    status = soup.find("b", string="Incarceration Status:")
    if not status:return None
    status = status.parent.find_next_sibling().getText(strip=True)
    if status == "INACTIVE" :return None
    location = soup.find("b", string="Current Location:")
    if not location: return None
    location = location.parent.find_next_sibling().getText(strip=True)
    if not location.endswith(" CI"): return None
    return location.removesuffix(" CI").split("-")[0]


def fetchFacilities():
    locationLinks = set()
    resp = requests.get(facilities_url, headers=safeHeaders())
    if resp.status_code != 200:
        raise Exception("location website could not be loaded at url", facilities_url)

    soup = BeautifulSoup(resp.text,'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href == None:
            continue
        if not href.startswith("/divisions-and-sections/prisons/prison-facilities/") and not href.startswith("/divisions-and-sections/institutions/prison-facilities/"):
            continue
        locationLinks.add(href)



    facilityMap = {}
    for link in locationLinks:
        resp = requests.get(state_url+link, headers=safeHeaders())
        if resp.status_code != 200:
            print("ERROR")
            raise Exception("location website could not be loaded at url", state_url+link)

        soup = BeautifulSoup(resp.text, 'html.parser')

        name = link.split("/")[-1].strip().split("-")[0].lower()

        containers = soup.find_all("strong")

        found = False

        for container in containers:
            if "Address:" in container.get_text() or "Street address" in container.get_text():
                address = container.next_sibling.get_text(strip=True).replace(u'\u200b', "").replace(u'\xa0', u' ')

                facilityMap[name]=address
                found = True
                break
        if not found:
            print("warning cant get address from: "+ link)
    return facilityMap


class NorthCarolinaScraper(AbstractStateScraper):
    def load(self, use_cache = True):
        print("initializing north carolino")
        file_path = "stateCache/NorthCarolina.json"
        if use_cache and os.path.exists(file_path): # Check if the file exists
            with open(file_path, 'r') as file:
                self.facilityMap = json.load(file) # Load data from the JSON file
            print("initialized north carolina from cache")
        else:
            print("initializing north carolina from web")
            self.facilityMap = fetchFacilities() # Fetch data if file doesn't exist
            print("initialized north carolina from web")
            if use_cache:
                with open(file_path, 'w') as file:
                    json.dump(self.facilityMap, file, indent=4) # Cache data to file_path
    def query(self, query: Query) -> list[type: PrisonMatch]:
        responses = []
        data = [process_id(query["inmate_id"])]
        if data[0] == None:
            data = fetch_name(query["first_name"], query["last_name"])
        
        for match in data:
            if match == None:
                continue
            unit = match.lower()
            address = self.facilityMap[unit] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"

            responses.append(PrisonMatch.create(f"{unit.upper()} UNIT", address, query["add1"]))
        return responses