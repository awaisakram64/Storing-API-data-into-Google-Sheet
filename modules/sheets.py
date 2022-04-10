

def update_sheet_data(sheet_client, sheet_id, values, range_name='Sheet1'):
    """append data into google sheet. """
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

def get_sheet_data(sheet_client, sheet_id, range_name='Sheet1'):
    """get data from google sheet. """
    try:
        result = sheet_client.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_name).execute()
        # print('{0} cells updated.'.format(result.get('updatedCells')))
        return result
    except Exception as e:
        print("exception in get_set_jobid: ",str(e))