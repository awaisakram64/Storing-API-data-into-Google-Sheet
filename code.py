import requests
import json
import pandas as pd
from datetime import date, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_data_from_api(date_received_min='', date_received_max='', days_ago=1, state='WA'):
    """this will get the required data from api

    """
    if any([date_received_min == '' , date_received_max=='']) and days_ago == 0:
        return 'missing parameters'

    server_endpoint = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/'
    headers = {
    'accept': 'application/json',
    }
    if days_ago > 0:
        date_received_min, date_received_max = calculate_start_and_end_date(days_ago=30)

    params = {
        'field': 'complaint_what_happened',
        # 'size': '100',
        'date_received_min': date_received_min,
        'date_received_max':  date_received_max,
        'state': state
    }
    response = requests.get(url=server_endpoint, headers=headers, params=params)
    data = response.json()
    complete_date = []
    for doc in data['hits']['hits'][:5]:
        doc_updated = doc['_source']
        doc_updated.update({'_id':doc['_id']})
        # print()
        # print(doc_updated)
        complete_date.append(doc_updated)
    return complete_date

def get_gcp_credentials():
    print('getting credientials')
    service_acc = open('ssh/creds_temp.json', 'r').read()
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_acc, strict=False),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return credentials


def update_sheet_data(sheet_client, sheet_id, values, range_name='Sheet1'):
    """append data into google sheet.
    """
    try:
        # sheet_id = '1_uBI3Bdf2go8bdEzIlUcRKraurq-D5mh4T9xJZE3UYk'
        body = {
            'values': values
        }
        result = sheet_client.spreadsheets().values().append(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        return 'success'
    except Exception as e:
        print("exception in get_set_jobid: ",str(e))

def calculate_start_and_end_date(days_ago):
    max_date = (date.today()).strftime("%Y-%m-%d")
    min_date = (date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    return min_date, max_date


def main():
    data = get_data_from_api(days_ago=1)
