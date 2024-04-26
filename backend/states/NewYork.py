from bs4 import BeautifulSoup
import requests
from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper
import json
import os

state_url = "https://doccs.ny.gov/"
name_query_url = "https://nysdoccslookup.doccs.ny.gov/IncarceratedPerson/SearchByName"
din_query_url = "https://nysdoccslookup.doccs.ny.gov/IncarceratedPerson/SearchByDin"


def initJson():
    return {"din":None,"nysid":None,"lastName":"","firstName":"","middleInitial":"","suffix":"","birthYear":"","userDisplayableMessage":None,"clickNextFlag":"","clickNextDin":""}
def safeHeaders():
    return {
        "Content-Type": "application/json",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }

def fetchDin(din):
    resp = requests.post(
        din_query_url,
        data=('"' + din + '"'),
        headers=safeHeaders())
    data = resp.json()
    if not "din" in data: return None
    if data["din"]!=din: return None
    return [data]

def fetchName(firstName, lastName):
    data = initJson()
    data["lastName"] = lastName

    resp = requests.post(
        name_query_url,
        json=data,
        headers=safeHeaders())
    
    matches = []
    while(True): #shouldnt run out of id space
        if resp.status_code !=200:
            break
        try:
            data = resp.json()
            if len(data["persons"])==0:
                break
            for person in data["persons"]:
                if person["name"]==lastName.upper() + ", " + firstName.upper():
                    matches.append(person)
                else:
                    if len(matches)>0:
                        return matches
            nextDIN = data["persons"][len(data["persons"])-1]["din"]
            data = initJson()
            data["clickNextDin"] = nextDIN
            data["clickNextFlag"] = "Y"
            resp = requests.post(
                name_query_url,
                json=data,
                headers=safeHeaders())
        except Exception as e:
            print(e)
            break

#status, facility

def fetchFacilities():
    #print("fetching NY facilities")

    locationLinks = set()
    page = 0 
    while(True):
        resp = requests.get(state_url+"facilities?page=" + str(page))
        if resp.status_code != 200:
            raise Exception("location website could not be loaded at url", state_url+"facilities?page=" + str(page))

        soup = BeautifulSoup(resp.text, 'html.parser')

        prev = len(locationLinks)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href == None:
                continue
            if not href.startswith("/location"):
                continue
            locationLinks.add(href)
        
        if len(locationLinks)==prev:
            break

        page += 1
     

    #print(str(len(locationLinks)) + " locations found, grabbing addresses...")

    facilityMap = {}
    #lastlen = 0
    for link in locationLinks:
        resp = requests.get(state_url+link)
        if resp.status_code != 200:
            raise Exception("location website could not be loaded at url", state_url+link)
    
        soup = BeautifulSoup(resp.text, 'html.parser')

        name = link.removeprefix("/location/").removesuffix("-correctional-facility")

        addressContainer = soup.find("p", {"class": "address"})
        address = ""
        for child in addressContainer.findChildren("span"):
            address += child.get_text().strip() + ", "
        address = address.removesuffix(", ")


        facilityMap[name.replace("-", " ").upper()] = address

        out = name + " found"
        #print(out + " " * max(0,lastlen-len(out)), end='\r')
        #lastlen = len(out)

    #print("facility map finished")
    #print(facilityMap)
    return facilityMap


class NewYorkScraper(AbstractStateScraper):
    def load(self, use_cache = True):
        print("initializing new york")
        file_path = "backend/stateCache/NewYork.json"
        if use_cache and os.path.exists(file_path): # Check if the file exists
            with open(file_path, 'r') as file:
                self.facilityMap = json.load(file) # Load data from the JSON file
            print("initialized new york from cache")
        else:
            print("initializing new york from web")
            self.facilityMap = fetchFacilities() # Fetch data if file doesn't exist
            print("initialized new york from web")
            if use_cache:
                with open(file_path, 'w') as file:
                    json.dump(self.facilityMap, file, indent=4) # Cache data to file_path
    def query(self, query: Query) -> list[type: PrisonMatch]:
        responses = []
        data = fetchDin(query["inmate_id"])
        if data == None:
            data = fetchName(query["first_name"], query["last_name"])

        
        for match in data:
            unit = match["facility"]
            address = self.facilityMap[unit] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"
            responses.append(PrisonMatch.create(f"{unit.upper()} UNIT", address, query["add1"]))
        return responses
