#!/usr/bin/python

import json
import pendulum

from googleapiclient.discovery import build, Resource
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
		print("Scheduling broadcasts...")
		broadcasts = schedule_broadcasts(youtube, [
			Broadcast("Friday PM", pendulum.FRIDAY, 19, 30),
			Broadcast("Saturday AM", pendulum.SATURDAY, 10, 00),
			Broadcast("Saturday PM", pendulum.SATURDAY, 13, 30),
		],
		{
			"kind": "youtube#liveBroadcast",
			"status": {
				"privacyStatus": "unlisted",
				"selfDeclaredMadeForKids": True
			}
		})

		print("Broadcasts scheduled successfully!")

		print("Adding broadcasts to playlist...")

		for broadcast in broadcasts:
			insert_resource_to_playlist(youtube, "PL1JHys0-uCP0VR2TITGtd4TU7tGIQUA7F", broadcast["id"])

		print("Broadcasts added to playlist successfully!")
	except HttpError as e:
		print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

# Authorize the request and store authorization credentials.
def get_authenticated_service() -> Resource:
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
	credentials = flow.run_console()
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_playlists(youtube: Resource):
	request = youtube.playlistItems().list(
		part = "id,contentDetails,snippet",
		playlistId = "PL1JHys0-uCP0VR2TITGtd4TU7tGIQUA7F"
	)
	response = request.execute()

	print(json.dumps(response, indent = 4))

def insert_resource_to_playlist(youtube: Resource, playlist_id: str, resource_id: str):
	request = youtube.playlistItems().insert(
		part = "id,contentDetails,snippet,status",
		body = {
			"snippet": {
				"playlistId": playlist_id,
				"resourceId": resource_id
			}
		}
	)
	response = request.execute()

	print(json.dumps(response, indent = 4))

def schedule_broadcasts(youtube: Resource, broadcasts: list[Broadcast], broadcast_body: dict) -> list[dict]:
	scheduled_broadcasts: list[dict] = []

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

		scheduled_broadcasts.append(schedule_stream_resp)

		print(json.dumps(schedule_stream_resp, indent = 4))

	return scheduled_broadcasts

if __name__ == "__main__":
	main()
	