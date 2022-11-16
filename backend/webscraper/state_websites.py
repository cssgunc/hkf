import typing
import urllib3

http = urllib3.PoolManager()


class StateWebsite(object):
    def __init__(self, url, post_ext: str, input_map: dict[str, type: str]):
        self.url = url
        self.post_ext = post_ext
        self.input_map = input_map

    # inputs data into website and submits, landing on response page
    def query_post(self, first_name: str, last_name: str, inmate_id: str, prison_name: str, add1: str, city: str, state: str, zip: str) -> dict | None:
        fields = {}

        def add_field(name, value):
            if name in self.input_map.keys():
                fields[self.input_map[name]] = value

        add_field("first_name", first_name)
        add_field("last_name", last_name)
        add_field("inmate_id", inmate_id)
        add_field("prison_name", prison_name)
        add_field("add1", add1)
        add_field("city", city)
        add_field("state", state)
        add_field("zip", zip)

        resp = http.request('POST', self.url + "/" + self.post_ext, fields=fields)
        return resp.data if resp.status == 200 else None

    # visits base website
    def get_page(self) -> str | None:
        resp = http.request('GET', self.url)
        if resp.status != 200:
            return None
        return resp.data if resp.status == 200 else None

state_websites = {}
state_websites["TX"] = StateWebsite("https://inmate.tdcj.texas.gov/InmateSearch/search.action", "search", {
    "first_name": "firstName",
    "last_name": "lastName"
})