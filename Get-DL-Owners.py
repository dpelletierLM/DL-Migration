#!/usr/bin/env python3

#import libraries
import requests
import json
from microsoftgraph.client import Client

clientId = "ed629446-39a5-4c06-90e5-266f636444b6"
clientSecret = ".A~LjDJHl01MaTGeEhQKdK8A~U_pEpz997"
tenantId = "08a83339-90e7-49bf-9075-957ccd561bf1"
#authTenant = common
#graphUserScopes = User.Read Mail.Read Mail.Send
scope = "https%3A%2F%2Fgraph.microsoft.com%2F.default"
redirectURL = "https://graph.microsoft.com"

client = Client('CLIENT_ID', 'CLIENT_SECRET', account_type='common') # by default common, thus account_type is optional parameter.

url = client.authorization_url("https://graph.microsoft.com", scope, state=None)
response = client.exchange_code(redirectURL, code)
