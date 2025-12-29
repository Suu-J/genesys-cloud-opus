import base64, requests, sys, json
import csv

CLIENT_ID = ''
CLIENT_SECRET = ''
ENVIRONMENT = 'mypurecloud.com'

# Base64 encode the client ID and client secret
authorization = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "ISO-8859-1")).decode("ascii")

# Prepare for POST /oauth/token request
request_headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
request_body = {
    "grant_type": "client_credentials"
}

# Get token
response = requests.post(f"https://login.{ENVIRONMENT}/oauth/token", data=request_body, headers=request_headers)

# Check response
if response.status_code == 200:
    print("Got token")
else:
    print(f"Failure, could not get token: {str(response.status_code)} - {response.reason}")
    sys.exit(response.status_code)

# Get JSON response body
response_json = response.json()

# Prepare for GET /api/v2/authorization/roles request
requestHeaders = {
    "Authorization": f"{response_json['token_type']} {response_json['access_token']}"
}

# Read conversation ids from the CSV file and store the result in a list
conversations = []
with open('test_ids.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        conversation_id = row['Conversation_ID']
        conversations.append((conversation_id, row))

# Process each conversation
for conversation_id, row in conversations:
    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordings", headers=requestHeaders)

    # Check response
    if response.status_code == 200:
        print("Got 200 response")
        row['success'] = 'Yes'
    else:
        print(f"Failure, couldn't fetch recordings for conversation {conversation_id}: {response.status_code} - {response.reason}")
        row['success'] = 'No'

    json_data = response.json()
    for item in json_data:
        media_uri = item["mediaUris"]["0"]["mediaUri"]

    filename = f"{conversation_id}.opus"

    response = requests.get(media_uri, stream=True)

    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"File downloaded successfully: {filename}")
    else:
        print(f"Download failed for conversation {conversation_id}: {response.status_code}")

    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/conversations/{conversation_id}/recordingmetadata", headers=requestHeaders)
    json_data = response.json()

    filename = f"{conversation_id}.opus_metadata.json"
    if response.status_code == 200:
        with open(filename, "w") as file:
            json.dump(json_data, file)
        print(f"Metadata JSON file saved successfully: {filename}")
    else:
        print(f"Failed to save metadata JSON file for conversation {conversation_id}: {response.status_code}")

# Write back all the rows to the CSV file
fieldnames = ['Conversation_ID', 'success']
with open('test_ids.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for conversation_id, row in conversations:
        writer.writerow(row)

print("\nDone")