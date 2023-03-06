import os.path

from bs4 import BeautifulSoup
import typing
import urllib3
from state_websites import state_websites, Response
from csv_handler import CSVHandler

http = urllib3.PoolManager()
output_csv = CSVHandler("output")
output_csv.add_row(["Fname", "Lname", "InmateID", "PrisonName", "ADD1", "City", "State", "ZIP", "Found in Inmate Search", "Same Address", "New Prison Name", "New Prison Address"])

# runs a query using data from csv
def query(first_name: str, last_name: str, inmate_id: str, prison_name: str, add1: str, city: str, state: str, zip: str) -> None:
    # get state-specific website
    website = state_websites[state]

    # package parameters
    query_data = {"first_name": first_name, "last_name": last_name, "inmate_id": inmate_id, "prison_name": prison_name,
            "add1": add1, "city": city, "state": state, "zip": zip}

    # query
    print(f"SENT QUERY {query_data}")
    responses: list[Response] = website.query(query_data)
    res_str = list(map(lambda r: str(r), responses))
    print(f"QUERY RESULTS {res_str}")

    # store result in csv
    csv_row = [first_name, last_name, inmate_id, prison_name, add1, city, state, zip, len(responses) != 0]
    if len(responses) > 0:
        csv_row.extend([responses[0].address_changed, responses[0].prison_name, responses[0].prison_address])
    output_csv.add_row(csv_row)


# TEST CODE
print(f"STARTED {os.path.basename(__file__)}")
query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107")
query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567")
query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880")
query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099")