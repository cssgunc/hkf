from bs4 import BeautifulSoup
import requests

from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper
import json
import os

def safeHeaders(cookie):
    return {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    }


def get_facility(soup: BeautifulSoup):
    institution_link = soup.find("strong", string="MOST RECENT INSTITUTION:")

    if institution_link:
        return str(institution_link.next_sibling).lower().strip()
    else:
        return None
    

def fetch_id(id):
    session = requests.Session()

    data = {"vDisclaimer": "True", "submit2": "I+agree+-+Go+to+the+Offender+Query"}

    response = session.post(
        "https://services.gdc.ga.gov/GDC/OffenderQuery/jsp/OffQryForm.jsp?Institution=",
        data=data,
    )

    cookies = session.cookies.get_dict()
    cookiestr = ""

    for key in cookies:
        cookiestr += key + "=" + cookies[key] + ";"

    data = {
        "vIsCookieEnabled": "Y",
        "vLastName": "",
        "vFirstName": "",
        "vGender": "",
        "vRace": "",
        "vAgeLow": "",
        "vAgeHigh": "",
        "vCurrentInstitution": "",
        "vAlias": "",
        "vMiddleName": "",
        "vHeightLow": "",
        "vHeightHigh": "",
        "vWeightLow": "",
        "vWeightHigh": "",
        "vEyeColor": "",
        "vHairColor": "",
        "vSMT": "",
        "vSentencedTo": "",
        "vOffense": "",
        "vCounty": "",
        "vOutput": "Detailed",
        "vScope": "",
        "vListType": "",
        "vDetailFormat": "Summary",
        "RecordsPerPage": "45",
        "vUnoCaseNoRadioButton": "UNO_NO",
        "vOffenderId": id,
        "NextPage": "2",
    }

    response = requests.post(
        "https://services.gdc.ga.gov/GDC/OffenderQuery/jsp/OffQryRedirector.jsp",
        data=data,
        headers=safeHeaders(cookiestr),
    )
    soup = BeautifulSoup(response.text, "html.parser")
    return get_facility(soup)


def fetch_name(firstname, lastname):
    session = requests.Session()

    data = {"vDisclaimer": "True", "submit2": "I+agree+-+Go+to+the+Offender+Query"}

    response = session.post(
        "https://services.gdc.ga.gov/GDC/OffenderQuery/jsp/OffQryForm.jsp?Institution=",
        data=data,
    )

    cookies = session.cookies.get_dict()
    cookiestr = ""

    for key in cookies:
        cookiestr += key + "=" + cookies[key] + ";"

    data = {
        "vIsCookieEnabled": "Y",
        "vLastName": lastname,
        "vFirstName": firstname,
        "vGender": "",
        "vRace": "",
        "vAgeLow": "",
        "vAgeHigh": "",
        "vCurrentInstitution": "",
        "vAlias": "",
        "vMiddleName": "",
        "vHeightLow": "",
        "vHeightHigh": "",
        "vWeightLow": "",
        "vWeightHigh": "",
        "vEyeColor": "",
        "vHairColor": "",
        "vSMT": "",
        "vSentencedTo": "",
        "vOffense": "",
        "vCounty": "",
        "vOutput": "Detailed",
        "vScope": "",
        "vListType": "",
        "vDetailFormat": "Summary",
        "RecordsPerPage": "45",
        "vUnoCaseNoRadioButton": "none",
        "vOffenderId": "",
        "NextPage": "2",
    }

    response = requests.post(
        "https://services.gdc.ga.gov/GDC/OffenderQuery/jsp/OffQryRedirector.jsp",
        data=data,
        headers=safeHeaders(cookiestr),
    )
    soup = BeautifulSoup(response.text, "html.parser")

    if soup.find_all(string="INCARCERATION DETAILS"):
        return [get_facility(soup)]

    all_forms = soup.find_all("form")

    filtered_forms = [
        form for form in all_forms if form.get("name", "").startswith("fm")
    ]

    ids = [link.findChild()["value"] for link in filtered_forms]

    return map(fetch_id, ids)

def fetchFacilities():
    facility_map = {}
    resp = requests.get("https://gdc.georgia.gov/locations")
    if resp.status_code != 200:
        raise Exception("location website could not be loaded at url", "https://gdc.georgia.gov/locations")
    soup = BeautifulSoup(resp.text, "html.parser")

    for tr in soup.find_all("tr"):
        name = tr.findChild().get_text(strip=True).lower()
        addy = tr.findChild().find_next_sibling().find_next_sibling().get_text(strip=True)
        facility_map[name] = addy
    return facility_map

class GeorgiaScraper(AbstractStateScraper):
    def load(self, use_cache = True):
        print("initializing georgia")
        file_path = "stateCache/Georgia.json"
        if use_cache and os.path.exists(file_path): # Check if the file exists
            with open(file_path, 'r') as file:
                self.facilityMap = json.load(file) # Load data from the JSON file
            print("initialized georgia from cache")
        else:
            print("initializing georgia from web")
            self.facilityMap = fetchFacilities() # Fetch data if file doesn't exist
            print("initialized georgia from web")
            if use_cache:
                with open(file_path, 'w') as file:
                    json.dump(self.facilityMap, file, indent=4) # Cache data to file_path
    def query(self, query: Query) -> list[type: PrisonMatch]:
        responses = []

        data = fetch_id(query["inmate_id"])
        if data == None or len(data) != 0:
            data = fetch_name(query["first_name"], query["last_name"])

        for match in data:
            if match==None:
                continue
            unit = match.lower()
            address = self.facilityMap[unit] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"

            responses.append(PrisonMatch.create(f"{unit.upper()} UNIT", address, query["add1"]))
        return responses