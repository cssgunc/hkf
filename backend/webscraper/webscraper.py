import os.path

from bs4 import BeautifulSoup
import typing
import urllib3
import threading
from state_websites import state_websites, Response, Query
from csv_handler import CSVHandler

http = urllib3.PoolManager()
output_csv = CSVHandler("output")
output_csv.add_row(["Fname", "Lname", "InmateID", "PrisonName", "ADD1", "City", "State", "ZIP", "Found in Inmate Search", "Same Address", "New Prison Name", "New Prison Address"])

lock = threading.Lock()


class QueryThread (threading.Thread):
    def __init__(self, query: Query):
        threading.Thread.__init__(self)
        self.query = query
        self.responses: list[Response] = []

    def run(self):
        website = state_websites[self.query.data["state"]]
        print(f"SENT QUERY {self.query.data}")
        self.responses = website.query(self.query)
        res_str = list(map(lambda r: str(r), self.responses))
        print(f"QUERY RESULTS {res_str}")


# runs a list of queries, exports as csv
def handle_queries(queries: list[Query]) -> None:
    # run query threads
    threads = [QueryThread(q) for q in queries]
    for t in threads:
        t.start()

    # store result in csv
    query_fields = ["first_name", "last_name", "inmate_id", "prison_name", "add1", "city", "state", "zip"]
    for t in threads:
        t.join()
        csv_row = [t.query.data[f] for f in query_fields]
        csv_row.append(len(t.responses) != 0)
        if len(t.responses) > 0:
            csv_row.extend([t.responses[0].address_changed, t.responses[0].prison_name, t.responses[0].prison_address])
        output_csv.add_row(csv_row)


# TEST CODE
print(f"STARTED {os.path.basename(__file__)}")
test_queries = [
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
    Query("CHRISTOPHER", "ALEMAN", "868445", "BILL CLEMENTS UNIT", "9601 SPUR 591", "AMARILLO", "TX", "79107"),
    Query("NATHANIEL", "AVILA", "862150", "PACK UNIT", "2400 WALLACE PACK RD", "NAVASOTA", "TX", "77868-4567"),
    Query("ANTONIO", "GOMEZ", "929416", "BETO UNIT", "1391 FM 3328, Tennessee Colony, TX 75880", "TENNESSEE COLONY", "TX", "75880"),
    Query("SAM", "LEOS", "410726", "HUGHES UNIT", "RT 2  BOX 4400", "GATESVILLE", "TX", "76597-0099"),
]
handle_queries(test_queries)