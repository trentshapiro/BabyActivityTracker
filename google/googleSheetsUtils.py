import urequests as requests
import json
import time
import secrets

# config
CLIENT_ID = secrets.CLIENT_ID
CLIENT_SECRET = secrets.CLIENT_SECRET
REFRESH_TOKEN = secrets.REFRESH_TOKEN
WORKBOOK_ID = secrets.WORKBOOK_ID

# constants
SPACE = " "

''' Given the refresh token, return the response which includes the access
    token and other bits of information.
'''
def refresh_access_token(refresh_tkn):
    url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    r = requests.request('POST', url, json=data)
    return r

''' Given a string message, row index and column index, return the payload of
    a cell.
'''
def a_cell(message, row, col):
    cell = {
        "updateCells": {
            "rows": [
                {
                    "values": [
                        {
                            "userEnteredValue": {
                                "stringValue": message
                            }
                        }
                    ]
                }
            ],
            "fields": "*",
            "start": {
                "sheetId": 0,
                "rowIndex": row,
                "columnIndex": col
            }
        }
    }
    return cell

''' Generate the request with the default intention of filling the entire row
    at `index` with the list of messages. If `row_fill` is set to `False`, 
    the column at `index` will be filled instead.
'''
def generate_request(messages, index, row_fill=True):
    requests = []
    if row_fill:
        for i in range(len(messages)):
            requests.append(a_cell(messages[i], index, i))
    # column fill
    else:
        for i in range(len(messages)):
            requests.append(a_cell(messages[i], i, index))
    return requests

class gsheets():

    def __init__(self, refresh_tkn):
        r = refresh_access_token(refresh_tkn)
        data = r.json()
        self.token = data["access_token"]
        self.token_type = data["token_type"]

    def write_cells(self, message, spreadsheet_id, cell_range):
        url = "https://sheets.googleapis.com/v4/spreadsheets/" \
            + f"{spreadsheet_id}/values/{cell_range}?valueInputOption=USER_ENTERED"
        
        body = {
            "range":cell_range,
            "majorDimension": "ROWS",
            'values':[message]
        }
        
        headers = {
            "Authorization": self.token_type + SPACE + self.token
        }

        r = requests.request("PUT", url, json=body, headers=headers)
        return r
    

    def get_cells(self, spreadsheet_id, cell_range):
        url = "https://sheets.googleapis.com/v4/spreadsheets/" \
            + f"{spreadsheet_id}/values/{cell_range}"

        headers = {
            "Authorization": self.token_type + SPACE + self.token
        }

        r = requests.request("GET", url, data=None, headers=headers)
        return r.json()['values'][0][0]

def main():
    # post all important info to Google Sheets
    message = [str(time.localtime())]
    gs = gsheets(REFRESH_TOKEN)
    
    # get cells max
    r = gs.get_cells(WORKBOOK_ID, 'Sheet1!B1')
    print(r)
    next_cell = int(r)+1
    next_cell_range = f'Sheet1!A{next_cell}'
    print(next_cell_range)
    # write to next cell
    r = gs.write_cells(message, WORKBOOK_ID, next_cell_range)
    print(r.json())
    

if __name__ == "__main__":
    main()
