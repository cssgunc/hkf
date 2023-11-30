from bs4 import BeautifulSoup
import urllib3
import requests
import re
from common import Response

from common import Query

http = urllib3.PoolManager(cert_reqs="CERT_NONE") # TODO: fix SSL certifications
urllib3.disable_warnings()

facilities_url = "https://www.cor.pa.gov/Facilities/StatePrisons/Pages/default.aspx"
location_url = "https://www.cor.pa.gov"
query_url = "https://captorapi.cor.pa.gov/InmLocAPI/api/v1/InmateLocator/SearchResults"

def safeHeaders():
    return {
        "Content-Type": "application/json",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }


def fetchFacilities():
    print("fetching PENN facilities")

    locationLinks = set()
    resp = http.request('GET', facilities_url)
    if resp.status != 200:
        raise Exception("location website could not be loaded at url", facilities_url)

    soup = BeautifulSoup(resp.data, 'html.parser')


    for link in soup.find_all('a'):
        href = link.get('href')
        if href == None:
            continue
        if not href.startswith("/Facilities/StatePrisons/Pages/"):
            continue
        locationLinks.add(href)
        

    

    print(str(len(locationLinks)) + " locations found, grabbing addresses...")

    facilityMap = {}
    lastlen = 0
    for link in locationLinks:
        resp = http.request('GET', location_url+link)
        if resp.status != 200:
            continue
        
        soup = BeautifulSoup(resp.data, 'html.parser')

        name = link.removeprefix("/Facilities/StatePrisons/Pages/").removesuffix(".aspx").replace("-", " ").upper()

        addressContainer = soup.find(string=re.compile('Facility Address:'))
        
        address = addressContainer.parent.get_text(separator=" ").strip().replace(u'\u200b', "").replace(u'\xa0', u' ')
        facilityMap[name] = address

        out = name + " found"
        print(out + " " * max(0,lastlen-len(out)), end='\r')
        lastlen = len(out)

    print("facility map finished")
    print(facilityMap)
    return facilityMap


class PennsylvaniaWebsite(object):
    def __init__(self):
        self.facilityMap = fetchFacilities()
    def query(self, query: Query) -> list[type: Response]:
        responses = []
        data = requests.post("https://captorapi.cor.pa.gov/InmLocAPI/api/v1/InmateLocator/SearchResults", headers=safeHeaders(),
            json={"id":query.data["inmate_id"],
                  "firstName":query.data["first_name"],
                  "lastName":query.data["last_name"],
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

        
        for match in data:
            unit = match["fac_name"]
            address = self.facilityMap[unit] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"

            responses.append(Response(f"{unit.upper()} UNIT", address, query.data["add1"]))
        return responses