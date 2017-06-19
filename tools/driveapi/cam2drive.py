# If you wish to use this program, contact jlaiman@purdue.edu for the 
# api oauth informationfrom __future__ import print_function

import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

all_dir_name = "'10 All images'"
cam_dir_name = "'11 Camera ID'"
dat_dir_name = "'12 Date Taken'"
unp_dir_name = "'13 Unprocessed Images'"
prn_dir_name = "'14 Processed Images, No Label'"
prl_dir_name = "'15 Processed Images, Labeled'"
dir_names = [all_dir_name, cam_dir_name, dat_dir_name, unp_dir_name, prn_dir_name, prl_dir_name]

all_dir_id = None
cam_dir_id = None
dat_dir_id = None
unp_dir_id = None
prn_dir_id = None
prl_dir_id = None
dir_ids = [all_dir_id, cam_dir_id, dat_dir_id, unp_dir_id, prn_dir_id, prl_dir_id]

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'CAM2 Image Manager'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'CAM2_IMG_MAN.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_folder_ids(service):
    # initialize main directory ID's that we'll need most
    for i in range(0,len(dir_ids)):
        results = service.files().list(
            q="name contains {0} and trashed = False".format(dir_names[i]),
            pageSize=2,
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('ERROR: File {0} not found.'.format(dir_names[i]))
        elif len(items) > 1:
            print('ERROR: More than one file found for {0}'.formatrange(dir_names[i]))
        else:
            dir_ids[i] = items[0]['id']

def main():
    """
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    get_folder_ids(service)

    for file in os.listdir('.'):
        if file.lower().endswith(('.png','.jpg','.jpeg')):
            media_body = MediaFileUpload(file, mimetype = 'image/png', resumable = True)
            body = {
                'name': file,
            }

            body['parents'] = [dir_ids[0]]

            try:
                 upload = service.files().create(
                    body = body,
                    media_body = media_body).execute()
            except errors.HttpError, error:
                print 'An error occured: %s' % error


if __name__ == '__main__':
    main()
