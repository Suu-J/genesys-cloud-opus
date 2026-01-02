import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from pprint import pprint

# OAuth credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
ENVIRONMENT = 'mypurecloud.com'
orgName = ''

# Configure API key authorization: PureCloud OAuth
PureCloudPlatformClientV2.configuration.host = 'https://login.mypurecloud.com/oauth/token'
api_client = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)

PureCloudPlatformClientV2.configuration.access_token = api_client.access_token

# Create an instance of the Recording API class
api_instance = PureCloudPlatformClientV2.RecordingApi()

conversation_id = '' # Replace with your conversation ID
max_wait_ms = 5000 # The maximum number of milliseconds to wait for the recording to be ready (optional)
format_id = 'OGG_OPUS' # The desired media format (optional)

try:
    # Get all of a Conversation's Recordings
    api_response = api_instance.get_conversation_recordings(conversation_id, max_wait_ms=max_wait_ms, format_id=format_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RecordingApi->get_conversation_recordings: %s\n" % e)

