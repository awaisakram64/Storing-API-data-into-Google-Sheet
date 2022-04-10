import json
from datetime import date, timedelta
from google.oauth2 import service_account

def get_gcp_credentials():
    """creating credentials object for authentication"""
    print('getting credientials')
    service_acc = open('ssh/creds_temp.json', 'r').read()
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_acc, strict=False),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return credentials

def calculate_start_and_end_date(days_ago):
    """calculate min and max date using days"""
    max_date = (date.today()).strftime("%Y-%m-%d")
    min_date = (date.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    return min_date, max_date