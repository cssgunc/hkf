from bs4 import BeautifulSoup
import requests
from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper
import json
import os



name_query_link = f'https://apps.cdcr.ca.gov/api/ciris/v1/incarceratedpersons?lastName=&firstName=&$limit=20&$sort[fullName]=1&$skip=0'
din_query_link = f'https://apps.cdcr.ca.gov/api/ciris/v1/incarceratedpersons/'
#by itself this din link will result in a 400 status error



def safeHeaders():
    return {
    "Host": "apps.cdcr.ca.gov",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Referer": "https://apps.cdcr.ca.gov/ciris/results?lastName=Smith",
    "Cookie": "_ga_3Z2V5385N6=GS1.1.1714084866.5.1.1714085449.0.0.0; _ga=GA1.2.1133773592.1713361124; _ga_PKEWHLJMFM=GS1.1.1714084866.6.1.1714085449.0.0.0; _clck=xai4gb%7C2%7Cfl8%7C0%7C1568; _gid=GA1.2.2034403115.1714003945; _clsk=17lspjr%7C1714085449317%7C11%7C1%7Cl.clarity.ms%2Fcollect; isActive=true",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "If-None-Match": "W/'2c29-1ZqIdxLE7AbPmRJCBjUVr9CEDK'"
    }

def fetchName(firstName, lastName) -> list:
    
    matches = []
    resp = requests.get(f'https://apps.cdcr.ca.gov/api/ciris/v1/incarceratedpersons?lastName={lastName}&firstName={firstName}&$limit=20&$sort[fullName]=1&$skip=0', headers=safeHeaders())
    newResp = resp.json()
    names = newResp['data']

    skipCounter = 0

    while(len(names) != 0):
        for name in names:
            test_name = lastName.upper() + ", " + firstName.upper()
            check_name = name['lastName'].upper() + ", " + name['firstName'].upper()
            if(test_name == check_name):
                matches.append(name)
        
        skipCounter += 1
        resp = requests.get(f'https://apps.cdcr.ca.gov/api/ciris/v1/incarceratedpersons?lastName={lastName}&firstName={firstName}&$limit=20&$sort[fullName]=1&$skip=' + str(skipCounter), headers=safeHeaders())
        newResp = resp.json()
        names = newResp['data']

    return matches


def fetchDin(din) -> list:
    
    resp = requests.get(f'https://apps.cdcr.ca.gov/api/ciris/v1/incarceratedpersons/{din}', headers=safeHeaders())
    if(resp.status_code >= 400):
        return None
    newResp = resp.json()
    if(din == newResp['cdcrNumber']):
        return [newResp]
    return None
    
    



class CaliforniaScraper(AbstractStateScraper):
    def load(self, use_cache = False):
        #no cache required
        pass
    def query(self, query: Query) -> list[type: PrisonMatch]:
        print('reaches scraper query')
        responses = []
        data = fetchDin(query["inmate_id"])
        if data == None:
            data = fetchName(query["first_name"], query["last_name"])

        for match in data:
            address = (match['locationAddress'] if match['locationAddress'] != None else f"UNIT: (unknown address)")
            name = (match['location'] if match['location'] != None else f"UNIT: (unknown name)")
            responses.append(PrisonMatch.create(f"{name.upper()} UNIT", address, query["add1"]))
        return responses
        
