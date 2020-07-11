from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("drive_config.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)


creds.refresh(Request())

service = build("drive", "v3", credentials=creds)

ANTI_THEFT_MEDIA_FOLDER_ID = None
response = (
    service.files()
    .list(q="mimeType='application/vnd.google-apps.folder'", spaces="drive")
    .execute()
)

for item in response.get("files", []):
    if item["name"] == "anti_theft_media":
        ANTI_THEFT_MEDIA_FOLDER_ID = item["id"]
if ANTI_THEFT_MEDIA_FOLDER_ID is None:
    file_metadata = {
        "name": "anti_theft_media",
        "mimeType": "application/vnd.google-apps.folder",
    }
    file = service.files().create(body=file_metadata, fields="id").execute()
    ANTI_THEFT_MEDIA_FOLDER_ID = file.get("id")
if ANTI_THEFT_MEDIA_FOLDER_ID is None:
    raise Exception("ANTI_THEFT_MEDIA_FOLDER_ID not found.")


def upload_file(full_file_name):
    file_name = os.path.basename(full_file_name)
    file_metadata = {
        "name": file_name,
        "mimeType": "*/*",
        "parents": [ANTI_THEFT_MEDIA_FOLDER_ID],
    }
    media = MediaFileUpload(full_file_name, mimetype="*/*", resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields="id").execute()
