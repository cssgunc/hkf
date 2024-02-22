import typing
from typing import Optional
from bs4 import BeautifulSoup
from abc import abstractmethod

from states import NewYork, Pennsylvania, Texas

from common import Response

from common import Query

import urllib3

http = urllib3.PoolManager(cert_reqs="CERT_NONE") # TODO: fix SSL certifications
urllib3.disable_warnings()

# maps state id to state website
state_websites = {
    "AL": None,                     # Alabama
    "AK": None,                     # Alaska
    "AZ": None,                     # Arizona
    "AR": None,                     # Arkansas
    "CA": None,                     # California
    "CO": None,                     # Colorado
    "CT": None,                     # Connecticut
    "DE": None,                     # Delaware
    "DC": None,                     # District of Columbia
    "FL": None,                     # Florida
    "GA": None,                     # Georgia
    "HI": None,                     # Hawaii
    "ID": None,                     # Idaho
    "IL": None,                     # Illinois
    "IN": None,                     # Indiana
    "IA": None,                     # Iowa
    "KS": None,                     # Kansas
    "KY": None,                     # Kentucky
    "LA": None,                     # Louisiana
    "ME": None,                     # Maine
    "MD": None,                     # Maryland
    "MA": None,                     # Massachusetts
    "MI": None,                     # Michigan
    "MN": None,                     # Minnesota
    "MS": None,                     # Mississippi
    "MO": None,                     # Missouri
    "MT": None,                     # Montana
    "NE": None,                     # Nebraska
    "NV": None,                     # Nevada
    "NH": None,                     # New Hampshire
    "NJ": None,                     # New Jersey
    "NM": None,                     # New Mexico
    "NY": NewYork.NewYorkWebsite(), # New York
    "NC": None,                     # North Carolina
    "ND": None,                     # North Dakota
    "OH": None,                     # Ohio
    "OK": None,                     # Oklahoma
    "OR": None,                     # Oregon
    "PA": Pennsylvania.PennsylvaniaWebsite(),# Pennsylvania
    "RI": None,                     # Rhode Island
    "SC": None,                     # South Carolina
    "SD": None,                     # South Dakota
    "TN": None,                     # Tennessee
    "TX": Texas.TexasWebsite(),           # Texas
    "UT": None,                     # Utah
    "VT": None,                     # Vermont
    "VA": None,                     # Virginia
    "WA": None,                     # Washington
    "WV": None,                     # West Virginia
    "WI": None,                     # Wisconsin
    "WY": None,                     # Wyoming
}