#!/usr/bin/env python3
from asyncore import write
from pprint import pprint
from tokenize import group
import requests
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
graph_URL = "https://graph.microsoft.com"

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

    response = requests.post(url=token_URL, headers=headers, data=body)
    response.raise_for_status()
    response_body = response.json()
    #response_object = json.loads(response_body)
    json_formmatted_str = json.dumps(response_body, indent=0)
    #print(response_body)
    #print(json_formmatted_str)
    authorization_token = f"{response_body['token_type']} {response_body['access_token']}"
    #print(authorization_token)
    return authorization_token # returns the authorization token value from the function block to the authorization token variable outside of this function so it can be

authorization_token = get_graph_access_token() # Sets authorization token variable to the value returned from get graph access token function

graph_URL = "https://graph.microsoft.com"

def get_groups(authorization_token):
    """Gets all groups in AD in Azure"""

    get_groups_URL = f'{graph_URL}/v1.0/groups'
    
    get_groups_headers = {
        'Authorization': authorization_token
    }

    get_groups_body = {
    }

    count = 0

    while True:
        if not get_groups_URL:
            break

        get_groups_response = requests.get(url=get_groups_URL, headers=get_groups_headers, data=get_groups_body)
        if get_groups_response.status_code == 200:
            get_groups_response.raise_for_status()
            json_data = json.loads(get_groups_response.text)
            get_groups_next_page = json_data["@odata.nextLink"] # Fetch next page

            get_groups_response_body = get_groups_response.json()
            get_groups_json_formmatted_str = json.dumps(get_groups_response_body, indent=0)
            group_ids = get_groups_response_body['value'] 
            
            g = open("PythonGroupIDoutput.txt", "w")
            g.write(get_groups_json_formmatted_str)
            g.close
            f = open("PythonOutput.txt", "a")
            
            for group in group_ids:
                f.write(group['id']+"\n")
                print(group['id'])
                count = count + 1

            f.close()

            print(count)
        #print(group_ids)

get_groups(authorization_token)