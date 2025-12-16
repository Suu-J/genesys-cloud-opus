#WORKING CODE! CONVERT THIS SO IT'S USEABLE FOR LARGE BATCHES
# WILL PRINT COUNTS FOR EACH ID
import requests
import base64
import sys
import csv
import codecs

CLIENT_ID = ''
CLIENT_SECRET = ''
ENVIRONMENT = 'mypurecloud.com'

authorization = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "ISO-8859-1")).decode("ascii")
request_headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
request_body = {
    "grant_type": "client_credentials"
}

response = requests.post(f"https://login.{ENVIRONMENT}/oauth/token", data=request_body, headers=request_headers)
if response.status_code != 200:
    print(f"Error getting token: {response.status_code} - {response.text}")
    sys.exit(response.status_code)

response_json = response.json()
access_token = response_json['access_token']

request_headers = {
    "Authorization": f"Bearer {access_token}"
}

conversations = []
with codecs.open('test_ids.csv', 'r', 'utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        conversation_id = row['id_list']
        conversations.append(conversation_id)

with codecs.open('recording_counts.csv', 'w', 'utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['conversation_id', 'recording_count'])
    writer.writeheader()

    for conversation_id in conversations:
        response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordings", headers=request_headers)
        
        if response.status_code == 200:
            recordings = response.json()
            recording_count = len(recordings)
            print(f"Conversation ID: {conversation_id} has {recording_count} recordings")
            writer.writerow({'conversation_id': conversation_id, 'recording_count': recording_count})
        else:
            print(f"Failed to fetch recordings for conversation {conversation_id}: {response.status_code} - {response.text}")
            writer.writerow({'conversation_id': conversation_id, 'recording_count': 'Error'})

print("\nDone")