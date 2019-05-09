'''
The purpose of the ETL is to flatten the results into a single row per parcel number
'''

import os,sys
import pandas as pd
from tqdm import tqdm

from record import Record


if __name__ == '__main__':
    
    fpath = os.path.join(".data", "2018 DUVAL COUNTY REAL COMBINED TAX ROLL CERTIFIED.TXT")

    outpath = os.path.join(".data", "casetable.psv")

    if os.path.exists(fpath) == False:
        raise ValueError("path " + fpath + " does not exist")

    sep = '|'
    lineno=0
    lastparcel = None
    recordcodes = ['00001', '00004', '00005', '00007' '00015', '00017']
    recordfields = {}
    
    recordfields["00001"] = [("Parcel Number", 2), ("Section", 3), ("Township", 4), ("Total Market Value", 22), ("Assessed Value", 23), ("Total Just Value", 25), ("doc acres", 31)]
    recordfields["00004"] = [("Site Address Number", 3), ("Site Address Street Name", 5), ("Site Address Street Type", 6), ("Site Address Unit Number", 7), ("Site Address City", 8), ("Site Zip Code", 9), ("Building Number", 10) ]
    recordfields["00005"] = [("building type code", 4), ("building style code", 6), ("building class code", 7), ("quality code", 8), ("actual year built", 9), ("effective year built", 10), ("building value", 12), ("building heated area", 13)]
    recordfields["00007"] = [("Number Of Bedrooms", 4), ("Number Of Bathrooms", 6), ("Number Of Rooms", 4), ("Number Of Stories", 4)]
    recordfields["00010"] = [("Amenity Item Code", 4)]
    recordfields["00015"] = [("Exemption Code", 5)]
    recordfields["00017"] = [("Date of Sale", 13), ("Sale Price", 15)]

    keys = ["00001", "00004", "00005", "00007", "00010", "00015", "00017"]

    #create the column headers
    column_headers = []
    for key in keys:
        column_headers.extend([x[0] for x in recordfields[key]])

    df = pd.DataFrame(columns=column_headers)

    record = Record()
    with open(fpath, 'r', encoding="ISO-8859-1") as f:
        for lineno, line in enumerate(tqdm(f)):

            if lineno % 10000 == 0:
                print("line #: %s" % lineno)

            cols = line.split(sep)

            #first column is the row type which defines the columns
            rowtype = cols[0]

            #keep reading if we do not care about this record code
            if rowtype not in recordfields:
                continue            

            if record.isreadyforinsert():

                if record.exemptioncode in ["HB", "HX"]:
                    df.loc[len(df)] = record.toarray()

                record = Record()                    

            #second column is the parcel number
            record.parcelnumber = cols[1]
            
            #skip over scenarios where 15 does not exist
            if rowtype == "00015" and len(cols) == 0:
                continue

            #read the columns for the fields
            col_lookup  = {t[1]:t[0] for t in recordfields[rowtype]}
            col_vals = None

            try:
                col_vals    = [cols[k-1] for k,v in col_lookup.items()]
            except Exception as ex:
                if rowtype != "00015":
                    raise ValueError("Error getting column values for rowtype {} because {} with cols {}".format(rowtype, str(ex), cols))

            #update a record structure
            record.update(rowtype, col_vals)

    df.to_csv(outpath, sep="|", header=True, index=False,)