#!/usr/bin/env python
##############################################################################
# Copyright (C) Zenoss, Inc. 2024, all rights reserved.
# Author: Team Pinecone
# Contact: Bill Loss 'closs  @ zenoss.com'
##############################################################################

import sys
import zenApiLib
import argparse
import requests
import json
import re
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description='grab host and zendesk user.')
parser.add_argument("-c", "--collector", action="store", dest="collector", required=True, help="Down Collector host ID")
parser.add_argument("-e", "--email", action="store", dest="email", required=True, help="ZenDesk user's email to be notified")
parser.add_argument("-E", "--evid", action="store", dest="evid", required=True, help="should be the current evid from evt/evid")
args = parser.parse_args()

# ToDo: convert to proper logging
print(args)

url = "https://zenoss1724961392.zendesk.com/api/v2/tickets"

payload = {
  "ticket": {
    "submitter_id": 29771010991501,
    "requester": args.email,
    "comment": {
      "body": "Collector host " + args.collector + " is no longer connected to Zenoss Cloud, please restart, yada yada."
    },
    "priority": "urgent",
    "type": "incident",
    "subject": "Collector host " + args.collector + " offline",
  }
}


headers = {
        "Content-Type": "application/json", 
        "Idempotency-Key": args.evid
}

# change me: should be zendesk automation user ie support@zenoss.com or automation@zenoss.com
email_address = 'closs@zenoss.com'
# change me to match above user
api_token = 'DeqYUrk7BCXBOE7V7Pehcw70oI5v37i58ZcDnoNh'
# Use basic authentication
#auth = HTTPBasicAuth(f'{email_address}/token', api_token)
auth = HTTPBasicAuth('{}/token'.format(email_address), api_token)

response = requests.request(
        "POST",
        url,
        auth=auth,
        headers=headers,
        json=payload
)

# ToDo: convert to proper logging
print(response.text)

decoded = response.json()
ticket_number = decoded['audit']['ticket_id']

# ToDo: convert to proper logging
print("Ticket Number: %s" % str(ticket_number))

# ToDo: url is hardcoded here but should probably be extracted from payload
url = "https://zenoss1724961392.zendesk.com/agent/tickets/" + str(ticket_number)
print("Ticket URL: %s" % url)

############################################ SET HOST TO MAINT HAPPENS IN SEPARATE SCRIPT########################

### Update event to store url and ticket_num as zenoss.IncidentManagement.url and zenoss.IncidentManagement.number

def updateEvent(**data):
#  import pdb; pdb.set_trace()
  zep = zenApiLib.zenConnector(routerName = "EventsRouter")
  response = zep.callMethod("updateDetails", **data)
  if response.get('result', {}).get('success', False) is False:
      raise Exception('API call returned unsucessful result.\n%s' % response)
  return response['result']

data =  {
            "evid" : args.evid,
            "zenoss.IncidentManagement.number" : str(ticket_number),
            "zenoss.IncidentManagement.url" : url
            }
        
api_response = updateEvent(**data)
# ToDo: convert to proper logging
print(data)
print(api_response)

