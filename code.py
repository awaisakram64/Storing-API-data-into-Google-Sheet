import requests
import pandas as pd
from googleapiclient.discovery import build
from modules.sheets import *
from modules.utility import *

def get_data_from_api(date_received_min='', date_received_max='', days_ago=20, state='WA'):
    """this will get the required data from api"""
    if any([date_received_min == '' , date_received_max=='']) and days_ago == 0:
        return 'missing parameters'

    server_endpoint = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/'
    headers = {
    'accept': 'application/json',
    }
    if days_ago > 0:
        date_received_min, date_received_max = calculate_start_and_end_date(days_ago=days_ago)

    params = {
        'field': 'complaint_what_happened',
        # 'size': '100',
        'date_received_min': date_received_min,
        'date_received_max':  date_received_max,
        'state': state
    }
    response = requests.get(url=server_endpoint, headers=headers, params=params)
    data = response.json()
    complete_date = pd.DataFrame()
    for doc in data['hits']['hits'][:5]:
        doc_updated = doc['_source']
        doc_updated.update({'_id':doc['_id']})
        # print()
        # print(doc_updated)
        complete_date = complete_date.append(doc_updated, ignore_index=True)
    return complete_date

def main():
    data = get_data_from_api(days_ago=10)
    credentials = get_gcp_credentials()
    sheet_client = build(
        'sheets', 'v4', 
        credentials=credentials,
        cache_discovery=False)
    range_name = 'Sheet1'
    sheet_id = 'YOUR SHEET ID'
    columns = list(data.columns)
    values = [list(i) for i in data.itertuples(index=False)]
    # getting data from sheet to check if data is already there or not
    results = get_sheet_data(sheet_client, sheet_id, range_name)
    if not results['values']:
        # if data is not present then adding the column as well.
        values.insert(0, columns)
    update_results = update_sheet_data(sheet_client, sheet_id, values, range_name)
    print(update_results)