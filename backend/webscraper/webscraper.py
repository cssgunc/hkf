from bs4 import BeautifulSoup
import typing
import urllib3
from state_websites import state_websites

http = urllib3.PoolManager()


# runs a query using data from csv
def query(first_name: str, last_name: str, inmate_id: str, prison_name: str, add1: str, city: str, state: str, zip: str) -> dict | None:
    website = state_websites[state]

    # query
    print("SENDING QUERY")
    data = website.query_post(first_name, last_name, inmate_id, prison_name, add1, city, state, zip)
    if data is None:
        return None
    soup = BeautifulSoup(data, "html.parser")

    # TEST CODE
    print("STORING OUTPUT")
    with open("test.html", "w") as f:
        f.write(soup.prettify())

    # return result
    return {}


# TEST CODE
print("START WEBSCRAPER.PY")
query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107")
