import requests
import json
import csv

csvfile = open('file.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = ("EVENT_NEWYEAR","EVENT_NONE","EVENT_SUPERBOWL","EVENT_THANKSGIVING", "EVENT_RAMADAN",
              "WEEKLY_MEAN_PRICE","ITEM_CATEGORY_ID", "ITEM_DEPARTMENT_ID",	"REGION_ID", "STORE_ID",
                "ITEM_ID", "YEAR", "MONTH",	"DAY", "DATE_STORE_ID_WEEKLY_SALES_MEAN_MA3",
                "DATE_STORE_ID_WEEKLY_SALES_SUM_LAG1", "DATE_REGION_ID_WEEKLY_SALES_SUM_LAG1",
                "DATE_ITEM_CATEGORY_ID_WEEKLY_SALES_SUM_LAG1")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')

URL = 'http://127.0.0.1:5000/prediccion'

result = requests.post(URL, json.dumps(jsonfile))
print(f"Result = {result.text}")