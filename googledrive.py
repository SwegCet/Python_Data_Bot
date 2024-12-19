import logging

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scope required for accessing google drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def getCredentials():
    creds = None
    try: 
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file('google_credentials.json', SCOPES)
        creds = flow.run_local_server()
        #Save the refresh token for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    #Check if Credentials are expired, refresh if necessary
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            #Save refreshed token
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
    return creds


#Authenticating Google API 
credentials = getCredentials()
service = build('drive', 'v3', credentials=credentials)


def createFolder(parentFolderId, folderName):
    #Define the folder metadata
    fileMetaData = {
        'name': folderName,
        'parents': [parentFolderId],
        'mimeType': 'application/vnd.google-apps.folder'
    }  
    
    #Create the folder
    folder = service.files().create(body=fileMetaData, fields='id').execute()
    
    return folder.get('id')


def uploadFile(folderId, filePath, fileName):
    media = MediaFileUpload(filePath, resumable=True)
    
    fileMetaData = {
        'name': fileName,
        'parents': [folderId]
    }
    
    request = service.files().create(body=fileMetaData, media_body= media, fields='id')
    
    logging.info(f"Uploading {fileName}. Please Wait...")
    
    #Upload File
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logging.info(f"Uploaded {int(status.progress() * 100)}%")
        
    logging.info(f"Uploaded {fileName}")
    