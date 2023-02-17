import os.path

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
    print(f"SENT QUERY {query_data}")
    results = website.query(query_data)
    print(f"QUERY RESULTS {results}")

    # return results
    return results


# TEST CODE
print(f"STARTED {os.path.basename(__file__)}")
query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107")
