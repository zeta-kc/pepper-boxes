#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

#from __future__ import print_function
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaFileUpload

import glob

# アップロードする画像の入っているフォルダ
IMG_DIR = './'

# アップロードするファイルの拡張子
EXTENSION = 'pdf'

# アップロードするファイルのMIMEタイプ
MIME_TYPE = 'application/pdf'

# Google Driveに作成するフォルダ名
DRIVE_DIR = 'pepper'

# アップロード先の親フォルダのID
# Google Driveでフォルダを開いた時のURLの末尾がフォルダID
# https://drive.google.com/drive/folders/ここがフォルダID
FOLDER_ID = 'my-drive'

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
        credentials = client.Credentials.new_from_json(os.environ.get('DRIVE_TOKEN', ''))
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
            if(single_file['name'] == 'schedule.pdf'):
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
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    uploader = GoogleDriveUploader()
    uploader.delete_file()
    uploader.upload_all_images()
