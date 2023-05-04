"""
Katrina Bennett
March 2023
Count number of lows in a given period of time from Nightscout data
"""

import requests
from datetime import datetime, timedelta

num_weeks = 4
count = num_weeks * 2016 #max number of readings per week
start_date = datetime.utcnow() - timedelta(weeks=num_weeks)
print("Counting number of lows since", start_date)
url = "https://keepinganeyeonkatrina.up.railway.app/api/v1/entries/?find[dateString][$gte]={}&count={}".format(start_date, count)
response = requests.get(url)

data, lows, currently_low, recorded = [], [], False, False

if response.status_code == 200:
    for row in response.text.strip().split("\n"):
        fields = row.strip().split("\t")
        entry = {
            "timestamp": fields[0],
            "sgv": int(fields[2]),
        }
        data.append(entry)
        
        if entry["sgv"] <= 70:
            if currently_low and not recorded:
                #count a low event as 2 or more consecutive readings under 3.9mmol/L
                lows.append(entry) 
                recorded = True
            else:
                currently_low = True
        elif entry["sgv"] > 80 and currently_low:
            #lows must be separated by at least one reading over 4.5mmol/L
            currently_low = False 
            recorded = False
else:
    print("Failed to fetch data from the API.")

#print(lows)
print("Total number of readings =", len(data))
print("Number of low events in last {} weeks =".format(num_weeks), len(lows))