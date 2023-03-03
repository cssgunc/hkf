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
query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567")
query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880")
query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099")