'''
PROCESSING OPUS FILES YO

had to encode the client id and client secret, i dont even remember why, ig the API needs it that way
Read conversation ids from the CSV file and store the result in a list
also struggled with BOM so use codecs to open the file with BOM removal

item["mediaUris"]["0"]["mediaUri"] -> json response for this api 
'''

import base64, requests, sys, json
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

if response.status_code == 200:
    print("Got token")
else:
    print(f"Failure, could not get token: {str(response.status_code)} - {response.reason}")
    sys.exit(response.status_code)

response_json = response.json()

# GET /api/v2/authorization/roles request
requestHeaders = {
    "Authorization": f"{response_json['token_type']} {response_json['access_token']}"
}

record_count = 1 # counter

conversations = []
with codecs.open('test_ids.csv', 'r', 'utf-8-sig') as csvfile:  
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['success'] != 'Yes':  # filtering process IDs with 'success' not marked as 'Yes'
            conversation_id = row['id_list']  # assuming the key is 'id_list' without the BOM here 
            conversations.append((conversation_id, row))

for conversation_id, row in conversations:
    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordings", headers=requestHeaders)
	
    print(f"\nrecord count number: {record_count}")
    record_count+=1
    if response.status_code == 200:
        print(f"Got 200 response for id: {conversation_id}")
        row['success'] = 'Yes'

        json_data = response.json()  # moved this block inside the 200 response check
        for item in json_data:
            media_uri = item["mediaUris"]["0"]["mediaUri"] # specific for this

        filename = f"{conversation_id}.opus" 

        response_media = requests.get(media_uri, stream=True)

        if response_media.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response_media.iter_content(1024):
                    file.write(chunk)
            print(f"File downloaded successfully: {filename}")
        else:
            print(f"Download failed for conversation {conversation_id}: {response_media.status_code}")

        response_metadata = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordingmetadata", headers=requestHeaders)
        json_data_metadata = response_metadata.json()

        filename_metadata = f"{conversation_id}.opus_metadata.json"
        if response_metadata.status_code == 200:
            with open(filename_metadata, "w") as file:
                json.dump(json_data_metadata, file)
            print(f"Metadata JSON file saved successfully: {filename_metadata}")
        else:
            print(f"Failed to save metadata JSON file for conversation {conversation_id}: {response_metadata.status_code}")

    else:
        print(f"Failure, couldn't fetch recordings for conversation {conversation_id}: {response.status_code} - {response.reason}")
        row['success'] = 'No'

fieldnames = ['id_list', 'success']
with open('updated_test_ids.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for conversation_id, row in conversations:
        writer.writerow(row)

print("\nDone")