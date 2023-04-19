import os.path

from bs4 import BeautifulSoup
import typing
import urllib3 # note: in the future if urllib3 is replaced with requests, use grequests as that can be multithreaded
import threading
from state_websites import Query, Response, state_websites
from csv_handler import CSVHandler

http = urllib3.PoolManager()
output_csv = CSVHandler("output")
output_csv.add_row(["Fname", "Lname", "InmateID", "PrisonName", "ADD1", "City", "State", "ZIP", "Found in Inmate Search", "Same Address", "New Prison Name", "New Prison Address"])

lock = threading.Lock()

# represents a thread running a single query
class QueryThread (threading.Thread):
    def __init__(self, query: Query):
        threading.Thread.__init__(self)
        self.query = query
        self.responses: list[Response] = []

    def run(self):
        website = state_websites[self.query.data["state"]]
        self.responses = website.query(self.query)
        res_str = list(map(lambda r: str(r), self.responses))


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
