""" Google Drive integration utility functions"""
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from django.conf import settings

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = settings.GOOGLE_DRIVE_CREDENTIALS_PATH


def authenticate():
    """ Returns Google Drive API service """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=credentials)
    return service


def get_team_drive_id(service):
    """ Finds team drive ID based on the name """
    if settings.GOOGLE_DRIVE_TEAM_DRIVE_ID:
        return settings.GOOGLE_DRIVE_TEAM_DRIVE_ID
    results = service.drives().list().execute()
    items = results.get("drives", [])
    for item in items:
        if item.name == settings.GOOGLE_DRIVE_TEAM_DRIVE_NAME:
            return item.id
    return None


def upload_to_team_drive(service, metadata, filepath):
    """ Uploads to team drive and returns ID """
    media = MediaFileUpload(filepath)
    team_drive_id = get_team_drive_id(service)
    uploaded = (
        service.files()
        .create(
            body=metadata, media_body=media, fields="id", supportsAllDrives=True
        )
        .execute()
    )
    return uploaded['id']
