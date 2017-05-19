# If you wish to use this program, contact jlaiman@purdue.edu for the 
# api oauth informationfrom __future__ import print_function

import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

cam_dir_name = "'11 Camera ID'"
dat_dir_name = "'12 Date Taken'"
unp_dir_name = "'13 Unprocessed Images'"
prn_dir_name = "'14 Processed Images, No Label'"
prl_dir_name = "'15 Processed Images, Labeled'"
dir_names = [cam_dir_name, dat_dir_name, unp_dir_name, prn_dir_name, prl_dir_name]

cam_dir_id = None
dat_dir_id = None
unp_dir_id = None
prn_dir_id = None
prl_dir_id = None
dir_ids = [cam_dir_id, dat_dir_id, unp_dir_id, prn_dir_id, prl_dir_id]

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
    # initialize directory ID's that we'll need most
    for i in range(0,5):
        results = service.files().list(
            q="name contains {0} and trashed = False".format(dir_names[i]),
            pageSize=10,
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('ERROR: File {0} not found.'.format(dir_names[i]))
        elif len(items) > 1:
            print('ERROR: More than one file found for {0}'.format(dir_names[i]))
        else:
            #print('success for {0}'.format(dir_names[i]))
            dir_ids[i] = items[0]['id']

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    get_folder_ids(service)



if __name__ == '__main__':
    main()
