import pandas as pd
import numpy as np

df = pd.read_excel('backend/Sample TX Data.xlsx')

#formatting inmate names
inmate_names = []

for f, l in zip(list(df["Fname"]), list(df["Lname"])):
    inmate_names.append(f + " " + l)


#getting inmate ids
ids = list(df["InmateID"])

for i in range(len(ids)):
    ids[i] = int(ids[i])


#reformatting addresses
addresses = []

for i in range(len(list(df["ADD1"]))):
    addr = list(df["ADD1"])[i]
    city = list(df["CITY"])[i]
    state = list(df["STATE"])[i]
    code = list(df["ZIP"])[i]

    address = addr + ", " + city + " " + state + ", " + code
    addresses.append(address)


modified_data = {"Name": inmate_names, "InmateID": ids, "Inmate Address": addresses}
inmate_data = pd.DataFrame(modified_data)


inmate_data.to_excel("backend/inmate_data.xlsx", index=False)