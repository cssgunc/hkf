from bs4 import BeautifulSoup
import typing
import urllib3
from state_websites import state_websites

http = urllib3.PoolManager()


# runs a query using data from csv
def query(first_name: str, last_name: str, inmate_id: str, prison_name: str, add1: str, city: str, state: str, zip: str) -> dict | None:
    # get state-specific website
    website = state_websites[state]

    # package parameters
    query_data = {"first_name": first_name, "last_name": last_name, "inmate_id": inmate_id, "prison_name": prison_name,
            "add1": add1, "city": city, "state": state, "zip": zip}

    # query
    print("SENDING QUERY")
    response_data = website.query(query_data)
    if (response_data == None):
        return None
    soup = response_data["landing_page"]

    # TEST CODE
    print("STORING OUTPUT")
    with open("webscraper/test.html", "w") as f:
        o = str(soup.prettify())
        o = o[o.find("<"):]
        f.write(o)

    # return result
    return {}


# TEST CODE
print("START WEBSCRAPER.PY")
query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107")
