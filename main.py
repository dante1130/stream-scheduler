#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3' 

def main():
	youtube = get_authenticated_service()
	try:
		list_streams(youtube)
	except HttpError as e:
		print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

# Authorize the request and store authorization credentials.
def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
  
# Retrieve a list of the liveStream resources associated with the currently
# authenticated user's channel.
def list_streams(youtube):
	print('Live streams:')

	list_streams_request = youtube.liveStreams().list(
		part='id,snippet',
		mine=True,
		maxResults=50
	) 

	while list_streams_request:
		list_streams_response = list_streams_request.execute()

	for stream in list_streams_response.get('items', []):
		print('%s (%s)' % (stream['snippet']['title'], stream['id']))

	list_streams_request = youtube.liveStreams().list_next(
		list_streams_request, list_streams_response)

if __name__ == '__main__':
	main()
	