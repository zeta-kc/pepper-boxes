#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaFileUpload

import glob

# アップロードする画像の入っているフォルダ
IMG_DIR = '/Users/zeta/Documents/Projects/pepper_boxes/backend/'

# アップロードするファイルの拡張子
EXTENSION = 'pdf'

# アップロードするファイルのMIMEタイプ
MIME_TYPE = 'application/pdf'

# Google Driveに作成するフォルダ名
DRIVE_DIR = 'pepper'

# client_secret.jsonの保存先
CLIENT_SECRET_FILE = 'client_secret_gdrive.json'

# アップロード先の親フォルダのID
# Google Driveでフォルダを開いた時のURLの末尾がフォルダID
# https://drive.google.com/drive/folders/ここがフォルダID
FOLDER_ID = 'my-drive'

# アプリケーション名
APPLICATION_NAME = 'PrintWithPepper'

# Google Driveにファイルの作成と、当該アプリで作成したファイルを取得できる権限(変更不要)
# その他の権限は以下のURLを参照: https://developers.google.com/drive/v3/web/about-auth
SCOPES = 'https://www.googleapis.com/auth/drive'


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GoogleDriveUploader:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v3', http=self.http)

        # /path/to/dir/*.jpg に一致するファイルを探しに行く
        self.file_path = os.path.join(IMG_DIR, '*.' + EXTENSION)
        self.files = glob.glob(self.file_path)
        if not self.files:
            print("No files to upload.")
            sys.exit()

    def get_credentials(self):
        u'''APIのQuickstartのコードのコピペ

        https://developers.google.com/drive/v3/web/quickstart/python
        初回実行時のみブラウザに認証画面が表示され、
        認証すると~/.credentials/に認証情報が保存される
        2回目以降は保存された認証情報を利用してアクセスする
        '''
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'drive-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
                print('Storing credentials to ' + credential_path)
        return credentials

    def create_folder(self):
        u'''Google Driveにフォルダを作成する'''
        print("Create folder: %s" % (DRIVE_DIR))
        file_metadata = {
            'name': DRIVE_DIR,
            'mimeType': 'application/vnd.google-apps.folder',
            # マイドライブ直下にフォルダを作成する場合は次の行をコメントアウト
            #'parents': [FOLDER_ID],
        }
        folder = self.service.files().create(body=file_metadata,
                                             fields='id').execute()
        # 作成されたフォルダのID
        self.sub_folder_id = folder.get('id')

    def upload_file(self, file_name):
        u'''ファイルをアップロードする'''
        media_body = MediaFileUpload(file_name, mimetype=MIME_TYPE, resumable=True)
        body = {
            'name': os.path.split(file_name)[-1],
            'mimeType': MIME_TYPE,
            # マイドライブ直下にファイルをアップロードする場合は次の行をコメントアウト
            #'parents': [self.sub_folder_id],
        }
        self.service.files().create(body=body, media_body=media_body).execute()

    def delete_file(self):
        result = self.service.files().list(
            pageSize=10,fields="nextPageToken, files(id, name)").execute()
        file_list = result['files']
        print(file_list)
        for single_file in file_list:
            if(single_file['name'] == 'out.pdf'):
                outpdf_id = single_file['id']
                print(outpdf_id)
                self.service.files().delete(fileId=outpdf_id).execute()

    def upload_all_images(self):
        u'''フォルダ内のファイルを全てアップロードする'''
        # マイドライブ直下にファイルをアップロードする場合は次の行もコメントアウト
        # self.create_folder()
        for file_name in self.files:
            print('upload: ' + file_name)
            self.upload_file(file_name)

if __name__ == '__main__':
    uploader = GoogleDriveUploader()
    uploader.delete_file()
    uploader.upload_all_images()
