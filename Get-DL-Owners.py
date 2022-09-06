#!/usr/bin/env python3
from pprint import pprint
from requests import post
import json
from datetime import datetime, date

from_date = date.today()
to_date = date.today()
timenow = datetime.now()
current_time = timenow.strftime("%H:%M:%S")

clientId = "ed629446-39a5-4c06-90e5-266f636444b6"
clientSecret = ".A~LjDJHl01MaTGeEhQKdK8A~U_pEpz997"
tenantId = "08a83339-90e7-49bf-9075-957ccd561bf1"
scopeInfo = "https%3A%2F%2Fgraph.microsoft.com%2F.default"
redirectURL = "https://graph.microsoft.com"

def get_graph_access_token():
    """Returns the access token needed to use API calls with MS Graph"""

    token_URL = f'https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token'

    headers = {
        'Host': 'login.microsoftonline.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }


    body = {
        'client_id': clientId,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': clientSecret,
        'grant_type': 'client_credentials',
        'tenant': tenantId
    }


    response = post(url=token_URL, headers=headers, data=body)
    response.raise_for_status()
    response_body = response.json()
    #response_object = json.loads(response_body)
    json_formmatted_str = json.dumps(response_body, indent=0)
    #print(response_body)
    print(json_formmatted_str)
    authorization_token = f"{response_body['token_type']} {response_body['access_token']}"

    print(authorization_token)

get_graph_access_token()

def get_groups():
    """Gets all groups in AD in Azure"""
    