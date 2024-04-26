from bs4 import BeautifulSoup
import requests
from query import Query, PrisonMatch
from abstractScraper import AbstractStateScraper
import json
import os


state_prisons_url = "https://fdc.myflorida.com/org/facilitydir.html"
dc_number_query = "https://fdc.myflorida.com/OffenderSearch/list.aspx?Page=List&TypeSearch=AI&DataAction=Filter&dcnumber="
last_name_query = "&LastName="
first_name_query = "&FirstName="
rest_link = "&SearchAliases=0&OffenseCategory=&photosonly=0&nophotos=1&matches=50"





def fetchName(firstName, lastName):
    matches = {}
    queryLink = dc_number_query + last_name_query + lastName +  first_name_query + firstName + rest_link
    resp = requests.get(queryLink)
    soup = BeautifulSoup(resp.text, "html")
    rows = soup.findAll("tr")
    for i in rows[1:]:
        data = i.findAll("td")
        row = [tr.text for tr in data]
        testString = lastName.upper() + ", " + firstName.upper()
        if testString not in row[1]:
            continue
        response = requests.get("https://fdc.myflorida.com" + data[0].a.get('href'))
        soup2 = BeautifulSoup(response.text, "html")
        url = soup2.find(id= "ctl00_ContentPlaceHolder1_trRow3")
        link = url.td.a.get("href")
        ref = link.find("#") + 1
        idA = link[ref:]
        matches[row[1]] = idA
    
        
        
    return matches



def fetchDin(din):
    matches2 = {}
    queryLink = dc_number_query + str(din) + last_name_query + first_name_query + rest_link
    resp = requests.get(queryLink)
    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.findAll("tr")
    #this will only iterate one time

    for i in rows[1:]:
        data = i.findAll("td")
        row = [tr.text for tr in data]
        testDin = str(din)
        if testDin not in row[2]:
            continue
        response = requests.get("https://fdc.myflorida.com" + data[0].a.get('href'))
        soup2 = BeautifulSoup(response.text, "html.parser")
        url = soup2.find(id= "ctl00_ContentPlaceHolder1_trRow3")
        link = url.td.a.get("href")
        ref = link.find("#") + 1
        idA = link[ref:]
        matches2[row[2]] = idA
        
    return matches2



def fetchFacilities() -> dict:
    prisonUrl = requests.get("https://fdc.myflorida.com/org/facilitydir.html")

    soup3 = BeautifulSoup(prisonUrl.text, 'html.parser')
    
    flag = False

    facilityMap: dict = {}
    for link in soup3.find_all("li"):
        try:
            
            idA = None
            if('Region 1 Office' in str(link.text).strip().split("\n")[0]):
                flag = True
            if("010 - PENSACOLA - CIRCUIT" in str(link.text).strip().split("\n")[0]):
                flag = False
            if(flag == True):
                if(link.a.get("id") != None):
                    idA = link.a.get('id')
                else:
                    idA = link.strong.a.get('id')
            
                var = str(link.text).strip().split("\n")
                if("Region" in var[0]):
                    continue
                newStr = ""
                contractString = var[1].replace("/r", "").strip().upper().replace(" ", "")
                if(contractString == "(CONTRACTFACILITY)"):
                    newStr0 = var[0].replace("\r", "") + ": "
                    newStr += var[2].replace("\r", "").strip()
                    newStr += " " + var[3].strip()
                    facilityMap[idA] = [newStr0, newStr]
                else:
                    newStr0 = var[0].replace("\r", "") + ": "
                    newStr += var[1].replace("\r", "").strip()
                    newStr += " " + var[2].strip()
                    facilityMap[idA] = [newStr0, newStr]
                
        except AttributeError:
            pass
    return facilityMap



class FloridaScraper(AbstractStateScraper):
    def load(self, use_cache = True):
        print("initializing florida")
        file_path = "backend/stateCache/Florida.json"
        if use_cache and os.path.exists(file_path): # Check if the file exists
            with open(file_path, 'r') as file:
                self.facilityMap = json.load(file) # Load data from the JSON file
            print("initialized florida from cache")
        else:
            print("initializing florida from web")
            self.facilityMap = fetchFacilities() # Fetch data if file doesn't exist
            print("initialized florida from web")
            if use_cache:
                with open(file_path, 'w') as file:
                    json.dump(self.facilityMap, file, indent=4) # Cache data to file_path
    def query(self, query: Query) -> list[type: PrisonMatch]:
        print('reaches scraper query')
        responses = []
        data = fetchDin(query["inmate_id"])
        if data == {}:
            data = fetchName(query["first_name"], query["last_name"])

        for match in data:
            unit = data[match]
            address = (self.facilityMap[unit])[1] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown address)"
            name = (self.facilityMap[unit])[0] if unit in self.facilityMap.keys() else f"UNIT: {unit} (unknown name)"
            responses.append(PrisonMatch.create(f"{name.upper()} UNIT", address, query["add1"]))
        return responses
        
