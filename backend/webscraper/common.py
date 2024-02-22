
# query
class Query:
    def __init__(self, first_name: str, last_name: str, inmate_id: str, prison_name: str, add1: str, city: str, state: str, zip: str):
        self.data = {"first_name": first_name, "last_name": last_name, "inmate_id": inmate_id, "prison_name": prison_name,
            "add1": add1, "city": city, "state": state, "zip": zip}


# response
class Response:
    # simple check to see if two addresses match
    def address_match(self, add1, add2) -> bool:
        add1 = add1.strip().lower()
        add2 = add2.strip().lower()
        if add1 == "" or add2 == "":
            return add1 == add2 == ""
        return add1 == add2 or add1 in add2 or add2 in add1

    # constructor
    def __init__(self, prison_name: str, prison_address: str, old_prison_address: str):
        self.address_changed = not self.address_match(prison_address, old_prison_address)
        self.prison_name = prison_name
        self.prison_address = prison_address

    # to_string method for debugging
    def __str__(self):
        return f"Response(address_changed: {self.address_changed}, prison_name: {self.prison_name}, prison_address: {self.prison_address})"