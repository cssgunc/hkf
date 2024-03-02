from typing import TypedDict


class Query(TypedDict):
    first_name: str
    last_name: str
    inmate_id: str
    prison_name: str
    add1: str
    city: str
    state: str
    zip: str

    @classmethod
    def create(
        self,
        first_name: str,
        last_name: str,
        inmate_id: str,
        prison_name: str,
        add1: str,
        city: str,
        state: str,
        zip: str,
    ):
        return Query(
            first_name=first_name,
            last_name=last_name,
            inmate_id=inmate_id,
            prison_name=prison_name,
            add1=add1,
            city=city,
            state=state,
            zip=zip,
        )


# simple check to see if two addresses match
def address_match(add1: str, add2: str) -> bool:
    add1 = add1.strip().lower()
    add2 = add2.strip().lower()
    if add1 == "" or add2 == "":
        return add1 == add2 == ""
    return add1 == add2 or add1 in add2 or add2 in add1


class PrisonMatch(TypedDict):
    found: str
    prison_name: str
    prison_address: str
    address_changed: str

    @classmethod
    def create(self, prison_name: str, prison_address: str, old_prison_address: str):
        return PrisonMatch(
            found="TRUE",
            prison_name=prison_name,
            prison_address=prison_address,
            address_changed=not address_match(prison_address, old_prison_address),
        )
    @classmethod
    def blank(self):
        return PrisonMatch(
            found="FALSE",
            prison_name="",
            prison_address="",
            address_changed="",
        )
    @classmethod
    def serialize(self, match):
        return {
            "Found in Inmate Search?": match["found"],
            "Same Address?": ("FALSE" if match["address_changed"] else "TRUE") if match["found"]=="TRUE" else "",
            "New Prison Name": match["prison_name"] if match["address_changed"] else "",
            "New Prison Address": match["prison_address"] if match["address_changed"] else "",
        }

    # to_string method for debugging
    def __str__(self):
        return f"PrisonMatch(address_changed: {self.address_changed}, prison_name: {self.prison_name}, prison_address: {self.prison_address})"
