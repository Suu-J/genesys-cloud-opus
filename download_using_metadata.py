#VERSION, THE METADATA IS FETCHED FIRST, AND THEN THE RECORDINGS ARE DOWNLOADED FROM THE IDs IN METADATA
'''
The API returns 202 after you request for the download
-> API returns 200 for transcoded recordings, and 202 for first time calls, 202 means currently transcoding
i think ideally it would have been better to trigger every single id, sleep for n seconds and then retrigger all


'''

import base64, requests, sys, json
import csv
import codecs

CLIENT_ID = ''
CLIENT_SECRET = ''
ENVIRONMENT = 'mypurecloud.com'

# auth requires base64 encoding to be put into request headers
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

requestHeaders = {
    "Authorization": f"{response_json['token_type']} {response_json['access_token']}"
}

record_count = 1
# reading conversation ids from the CSV file and store the result in a list
conversations = []
with codecs.open('test_ids.csv', 'r', 'utf-8-sig') as csvfile: 
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['success'] != 'Yes': 
            conversation_id = row['id_list']  # Assuming the key is 'id_list' without the BOM
            conversations.append((conversation_id, row))

for conversation_id, row in conversations:
    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordingmetadata", headers=requestHeaders)
	
    print(f"\nrecord count number: {record_count}")
    record_count+=1
    if response.status_code == 200:
        
        json_data = response.json() 
        
        # we need the recording id only
        for item in json_data:
            recording_id = item["id"]

        # but the file will be stored with conversation id as the name
        filename = f"{conversation_id}.opus"

        # Some IDs do not have metadata, in which case we just mark the row accordingly and move on to next Conversation ID
        if(len(json_data) == 0):
            print("its empty")
            row['success'] = 'RID missing'
            continue
        
        #use this recording_id for another API call using the recordingID, this api provides download link
        response_second = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordings/{recording_id}?formatId=MP3&emailFormatId=NONE&chatFormatId=NONE&messageFormatId=NONE&download=true&fileName={conversation_id}",headers=requestHeaders)


        if(response_second.status_code == 200):
            # API returns 200 for transcoded recordings, and 202 for first time calls, 202 means currently transcoding
            print(f"Status 200 for Recording ID call {recording_id}")
            row['success'] = 'Yes'

            json_data_second = response_second.json()
            # download link is termed as media uri and its nested within the json
            media_uri = json_data_second["mediaUris"]["S"]["mediaUri"]
            
            response_media = requests.get(media_uri, stream=True)
            if response_media.status_code == 200:
                with open(filename, "wb") as file:
                    for chunk in response_media.iter_content(1024):
                        file.write(chunk)
                print(f"File downloaded successfully: {filename}")
            else:
                print(f"Download failed for conversation {conversation_id}: {response_media.status_code}")
        # This is for when cloud is transcoding it still        
        elif(response_second.status_code == 202):
            print(f"rid 202 for Recording ID {recording_id}, Check Later")
            row['success'] = 'rid 202'
        # Rare 404 case where there is no recording for the conversation ID
        else:
            print(f"RID Failure, couldn't fetch data for conversation {recording_id}: {response_second.status_code} - {response_second.reason}")
            row['success'] = 'NO rid'

    # 202 for Metadata Usually doesn't occur tbh
    elif(response.status_code==202):
        print(f"Metadata Status Code 202, Try later for cid: {conversation_id}")
        row['success'] = 'Meta 202'
    # Some Recordings are missing
    else:
        print(f"Metadata Failure, couldn't fetch data for conversation {conversation_id}: {response.status_code} - {response.reason}")
        row['success'] = 'NO Meta'

fieldnames = ['id_list', 'success']
with open('updated_test_ids.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for conversation_id, row in conversations:
        writer.writerow(row)

print("\nFin.")
