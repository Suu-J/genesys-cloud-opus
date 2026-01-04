import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from pprint import pprint

# OAuth credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
ENVIRONMENT = 'mypurecloud.com'
orgName = ''
apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_saml2bearer_token(CLIENT_ID, CLIENT_SECRET,orgName)
usersApi = PureCloudPlatformClientV2.UsersApi(apiclient)
print(usersApi.get_users_me())
