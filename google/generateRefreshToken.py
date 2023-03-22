''' This script has been prepared for obtaining the access token and 
    refresh token for Google services such as Google Sheets API. By following
    the steps below you can achieve the results in my video.
    Source: https://docs.informatica.com/integration-cloud/cloud-data-integration-connectors/current-version/google-sheets-connector/introduction-to-google-sheets-connector/administration-of-google-sheets-connector/generating-oauth-2-0-access-tokens.html
'''


import urequests as requests
import secrets
import network
import ujson

# internet
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_NAME, secrets.WIFI_PWD)
if wlan.isconnected():
    print('Connected to {}'.format(secrets.WIFI_NAME))

# step 1: fill in the client credentials
CLIENT_ID = secrets.CLIENT_ID
CLIENT_SECRET = secrets.CLIENT_SECRET

# step 2: get a temporary access code manually
# https://accounts.google.com/o/oauth2/auth?access_type=offline&approval_prompt=auto&client_id=<<your-client-id>>&response_type=code&scope=https://www.googleapis.com/auth/spreadsheets&redirect_uri=http://localhost

ACCESS_CODE = secrets.ACCESS_CODE

# step 3: run this script
def main():
    # get refresh token/access token from access code
    url = "https://www.googleapis.com/oauth2/v4/token"
    data = {
        "code": ACCESS_CODE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "http://localhost",
        "grant_type": "authorization_code",
        "scope": "https://www.googleapis.com/auth/spreadsheets"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    r = requests.request("POST", url, json=data, headers=headers)
    print(r.text)

if __name__ == "__main__":
    main()
