import requests
import base64
import sys
import csv
import codecs

# Configuration variables...
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
    conversations = [row for row in reader]  # Load all conversations

# recording counts file with new successful entries
recording_counts_fieldnames = ['conversation_id', 'recording_count']
try:
    with codecs.open('recording_counts.csv', 'x', 'utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=recording_counts_fieldnames)
        writer.writeheader()
except FileExistsError:
    pass  # if file already exists, we'll append without writing the header
# total = len(conversations)
count=0
for row in conversations:
    # print(f"\nrecords left {total}")
    # total-=1
    if row['success'] not in ['Yes', 'Skip']:
        print(count)
        count+=1
        conversation_id = row['id_list']
        response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordings", headers=request_headers)
        
        if response.status_code == 200:
            recordings = response.json()
            recording_count = len(recordings)
            print(f"Conversation ID: {conversation_id} has {recording_count} recordings")
            row['success'] = 'Yes'
            with codecs.open('recording_counts.csv', 'a', 'utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=recording_counts_fieldnames)
                writer.writerow({'conversation_id': conversation_id, 'recording_count': recording_count})
        elif response.status_code == 202:
            print(f"Processing recordings for Conversation ID: {conversation_id}")
            row['success'] = 'No'
        elif response.status_code == 404:
            print(f"No recordings found for Conversation ID: {conversation_id}")
            row['success'] = 'Skip'
        else:
            print(f"Failed to fetch recordings for conversation {conversation_id}: {response.status_code} - {response.text}")
            row['success'] = 'Error'

with codecs.open('test_ids.csv', 'w', 'utf-8-sig') as csvfile:
    fieldnames = ['id_list', 'success']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(conversations)

print("\nDone")