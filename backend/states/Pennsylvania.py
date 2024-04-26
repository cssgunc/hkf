from bs4 import BeautifulSoup
import requests
import re
import os
import json
from query import Query, PrisonMatch

facilities_url = "https://www.cor.pa.gov/Facilities/StatePrisons/Pages/default.aspx"
location_url = "https://www.cor.pa.gov"
query_url = "https://captorapi.cor.pa.gov/InmLocAPI/api/v1/InmateLocator/SearchResults"

def safeHeaders():
    return {
        "Content-Type": "application/json",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }


def fetchFacilities():
    #print("fetching PENN facilities")

    locationLinks = set()
    resp = requests.get(facilities_url, verify=False)
    if resp.status_code != 200:
        raise Exception("location website could not be loaded at url", facilities_url)

    soup = BeautifulSoup(resp.text, 'html.parser')


    for link in soup.find_all('a'):
        href = link.get('href')
        if href == None:
            continue
        if not href.startswith("/Facilities/StatePrisons/Pages/"):
            continue
        locationLinks.add(href)
        

    

    #print(str(len(locationLinks)) + " locations found, grabbing addresses...")

    facilityMap = {}
    #lastlen = 0
    for link in locationLinks:
        resp = requests.get(location_url+link, verify=False)
        if resp.status_code != 200:
            continue
        
        soup = BeautifulSoup(resp.text, 'html.parser')

        name = link.removeprefix("/Facilities/StatePrisons/Pages/").removesuffix(".aspx").replace("-", " ").upper()

        addressContainer = soup.find(string=re.compile('Facility Address:'))
        
        address = addressContainer.parent.get_text(separator=" ").strip().replace(u'\u200b', "").replace(u'\xa0', u' ')
        facilityMap[name] = address

        out = name + " found"
        #print(out + " " * max(0,lastlen-len(out)), end='\r')
        #lastlen = len(out)

    #print("facility map finished")
    #print(facilityMap)
    return facilityMap


class PennsylvaniaScraper(object):
    def load(self, use_cache = True):
        print("initializing Pennsylvania")
        file_path = "backend/stateCache/Pennsylvania.json"
        if use_cache and os.path.exists(file_path): # Check if the file exists
            with open(file_path, 'r') as file:
                self.facilityMap = json.load(file) # Load data from the JSON file
            print("initialized Pennsylvania from cache")
        else:
            print("initializing Pennsylvania from web")
            self.facilityMap = fetchFacilities() # Fetch data if file doesn't exist
            print("initialized Pennsylvania from web")
            if use_cache:
                with open(file_path, 'w') as file:
                    json.dump(self.facilityMap, file, indent=4) # Cache data to file_path
    def query(self, query: Query) -> list[type: PrisonMatch]:
        responses = []
        data = requests.post("https://captorapi.cor.pa.gov/InmLocAPI/api/v1/InmateLocator/SearchResults", headers=safeHeaders(),
            json={"id":query["inmate_id"],
                  "firstName":query["first_name"],
                  "lastName":query["last_name"],
                  "middleName":"",
                  "paroleNumber":"",
                  "countylistkey":"---",
                  "citizenlistkey":"---",
                  "racelistkey":"---",
                  "sexlistkey":"---",
                  "locationlistkey":"---",
                  "age":"",
                  "dateofbirth":None,
                  "sortBy":"1"}
        )
        data = data.json()["inmates"]

        print(data)
        
        for match in data:
            unit = match["fac_name"]
            address = self.facilityMap[unit] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"

            responses.append(PrisonMatch.create(f"{unit.upper()} UNIT", address, query["add1"]))
        return responses