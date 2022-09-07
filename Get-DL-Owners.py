#!/usr/bin/env python3

from asyncore import write
from itertools import count
from pprint import pprint
from tokenize import group
import requests
import json
from datetime import datetime, date

#-------Define Variables----------
from_date = date.today()
to_date = date.today()
timenow = datetime.now()
current_time = timenow.strftime("%H:%M:%S")

clientId = "ed629446-39a5-4c06-90e5-266f636444b6"
clientSecret = ".A~LjDJHl01MaTGeEhQKdK8A~U_pEpz997"
tenantId = "08a83339-90e7-49bf-9075-957ccd561bf1"
scopeInfo = "https%3A%2F%2Fgraph.microsoft.com%2F.default"
graph_URL = "https://graph.microsoft.com"

group_IDs = []
group_owners = []

#------Define Functions---------

#Get access token for Graph API connections
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

#Get Groups from Azure AD using Graph API
def get_groups(authorization_token):
    """Gets all groups in AD in Azure"""
    page = 1
    get_groups_URL = f'{graph_URL}/v1.0/groups'
    group_IDs.append("GroupID," + "GroupTypes,"+"GroupDisplayName," + "GroupEmail") # Add column headers to list
    get_groups_headers = {
        'Authorization': authorization_token
    }

    get_groups_body = {
    }

    while True:
        if not get_groups_URL:
            break

        get_groups_response = requests.get(url=get_groups_URL, headers=get_groups_headers, data=get_groups_body)
        if get_groups_response.status_code == 200:            
            json_data = json.loads(get_groups_response.text)
            get_groups_next_page = json_data["@odata.nextLink"] # Fetch next page
            get_groups_URL = get_groups_next_page
            

            get_groups_response_body = get_groups_response.json()
            #Format JSON to make it easier to read and output it to a file
            get_groups_json_formmatted_str = json.dumps(get_groups_response_body, indent=0)
            get_group_output = open("PythonGroupInfoOutput.txt", "a") # Open file to write JSON output to
            get_group_output.write(get_groups_json_formmatted_str)
            get_group_output.close # Close file
            print("Page "+str(page))
            group_values = get_groups_response_body['value'] 
            for item in group_values:

                get_group_ID_Info = open("PythonGroupIDOutput.txt", "a") # Open file to append items to
                group_ID = item['id']
                group_Type = item['groupTypes']
                group_displayName = item['displayName']
                group_mail = item['mail']
                #print(group_ID)
                #print(group_Type)
                #print(group_displayName)
                #print(group_mail)
                #Write group info to file
                get_group_ID_Info.write(str(group_ID))
                get_group_ID_Info.write(",")
                get_group_ID_Info.write(str(group_displayName))
                get_group_ID_Info.write(",")
                get_group_ID_Info.write(str(group_mail))
                get_group_ID_Info.write(",")
                get_group_ID_Info.write(str(group_Type))
                get_group_ID_Info.write(",")
                get_group_ID_Info.write('\n')

                get_group_ID_Info.close # Close file 

                group_IDs.append({'Group_ID': group_ID, 'group_displayName': group_displayName, 'group_mail': group_mail, 'group_Type': group_Type})  
            page = page + 1
            print("Page is now "+ str(page))
        return group_IDs 
             
#Get List of Group Owners Using Graph API
def get_owners():
    write("not complete")

#-------Start Script--------

authorization_token = get_graph_access_token() # Sets authorization token variable to the value returned from get graph access token function

get_group_IDs = get_groups(authorization_token)
#print(get_group_IDs)
#print("Group ID Info above")
