#!/usr/bin/python

import pendulum

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from broadcast import Broadcast

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3" 

def main():
	youtube = get_authenticated_service()
	try:
		schedule_broadcasts(youtube)
	except HttpError as e:
		print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

# Authorize the request and store authorization credentials.
def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def schedule_broadcasts(youtube):
	print("Scheduling broadcast...")

	broadcasts = [
		Broadcast("Friday PM", pendulum.FRIDAY, 19, 30),
		Broadcast("Saturday AM", pendulum.SATURDAY, 10, 00),
		Broadcast("Saturday PM", pendulum.SATURDAY, 13, 30),
	]

	broadcast_body = {
		"kind": "youtube#liveBroadcast",
		"status": {
			"privacyStatus": "unlisted",
			"selfDeclaredMadeForKids": True
		}
	}

	for broadcast in broadcasts:
		broadcast_body["snippet"] = {
			"title": broadcast.title,
			"scheduledStartTime": broadcast.get_start_time(),
		}

		schedule_broadcast_req = youtube.liveBroadcasts().insert(
			part = "id,snippet,status",
			body = broadcast_body
		)

		schedule_stream_resp = schedule_broadcast_req.execute()

		print(schedule_stream_resp)

if __name__ == "__main__":
	main()
	