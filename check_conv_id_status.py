import base64, time, requests, sys, os, datetime
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from pprint import pprint


print("---------------------------------------------------")
print("- Genesys Cloud Python Client Checking Script -")
print("---------------------------------------------------")

CLIENT_ID = ''
CLIENT_SECRET = ''

# Base64 encode the client ID and client secret

authorization = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "ISO-8859-1")).decode("ascii")

print(authorization)
# Prepare for POST /oauth/token request
request_headers = {
    "Authorization": "Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
request_body = {
    "grant_type": "client_credentials"
}


# Get token
response = requests.post("https://login.mypurecloud.com/oauth/token", data=request_body, verify=False, allow_redirects=False,auth=(CLIENT_ID, CLIENT_SECRET))

print(str(response.status_code))
# Check response
if response.status_code == 200:
    print("Got token Successfully")
else:
    print(str(response.status_code) + "Failure:"+str(response.status_code)+"-"+response.reason)
    sys.exit(response.status_code)

#---------------------------------Assign the token to the Pure Colud -------------

# Get JSON response body
response_json = response.json()


response_token=response_json['access_token']
print( "Token:"+response_token)

# Configure OAuth2 access token for authorization: PureCloud OAuth
PureCloudPlatformClientV2.configuration.access_token = response_token
# or use get_client_credentials_token(...), get_saml2bearer_token(...) or get_code_authorization_token(...)

#--------------------------Recording------------------------------

current_datetime = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
interval_1 = sys.argv[1]
interval_2 = sys.argv[2]
con_interval = interval_1 + '/' + interval_2
print(con_interval)

# Get the api
recording_api = PureCloudPlatformClientV2.RecordingApi()

# Build the create job query, for export action, set query.action = "EXPORT"
query = PureCloudPlatformClientV2.RecordingJobsQuery()
query.action = "EXPORT"
query.action_date = current_datetime
# Comment out integration id if using DELETE
query.integration_id = "22dfccfe-71ad-4de4-a28f-4e965d0381d8"
query.conversation_query = {
    "interval": con_interval,
    "order": "asc",
    "orderBy": "conversationStart"
}
print(query)
try:
    # Call create_recording_job api
    create_job_response = recording_api.post_recording_jobs(query)
    job_id = create_job_response.id
    print("Successfully created recording bulk job", create_job_response)
    print(job_id)
except ApiException as e:
    print("Exception when calling RecordingApi->post_recording_jobs: { e }")
    sys.exit()


# Call get_recording_job api
while True:
    try:
        get_recording_job_response = recording_api.get_recording_job(job_id)
        job_state = get_recording_job_response.state
        if job_state != 'PENDING':
            break
        else:
            print("Job state PENDING...")
            time.sleep(2)
    except ApiException as e:
        print("Exception when calling RecordingApi->get_recording_job: { e }")
        sys.exit()


if job_state == 'READY':
    try:
        execute_job_response = recording_api.put_recording_job(job_id, {"state": "PROCESSING"})
        job_state = execute_job_response.state
        print("Successfully execute recording bulk job", execute_job_response)
    except ApiException as e:
        print("Exception when calling RecordingApi->put_recording_job: { e }")
        sys.exit()
else:
    print("Expected Job State is: READY, however actual Job State is: { job_state }")

# Call delete_recording_job api
# Can be canceled also in READY and PENDING states

if job_state == 'PROCESSING':
    try:
        cancel_job_response = recording_api.delete_recording_job(job_id)
        print("Successfully cancelled recording bulk job { cancel_job_response}")
    except ApiException as e:
        print("Exception when calling RecordingApi->delete_recording_job: { e }")
        sys.exit()

try:
    get_recording_jobs_response = recording_api.get_recording_jobs(
        page_size=25,
        page_number=1,
        sort_by="userId",  # or "dateCreated"
        state="",  # valid values FULFILLED, PENDING, READY, PROCESSING, CANCELLED, FAILED
        show_only_my_jobs=True,
        job_type="EXPORT",  # or "DELETE"
    )
    print("Successfully get recording bulk jobs", get_recording_jobs_response)
except ApiException as e:
    print("Exception when calling RecordingApi->get_recording_jobs: { e }")
    sys.exit()
