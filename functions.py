import pandas as pd
import streamlit as st
import os
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import configs


def write_to_google(df, gcp_service_account, sheet_key, sheet_name):

    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    credentials = service_account.Credentials.from_service_account_info(
        gcp_service_account, scopes=scopes)

    gc = gspread.authorize(credentials)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    # open a google sheet
    gs = gc.open_by_key(sheet_key)

    worksheet = gs.worksheet(sheet_name)

    if len(worksheet.get("A1")) == None:
        set_with_dataframe(worksheet=worksheet, dataframe=df,
                           include_index=False, include_column_header=True, resize=True)

    else:
        df_values = df.values.tolist()
        gs.values_append(sheet_name, {'valueInputOption': 'RAW'}, {
                         'values': df_values})

    return True


def check_inputs(input_list):
    for i in input_list:
        if i == "" or i == None:
            return False
        else:
            return True


def alpha_list(relative_path, sep):
    a_list = sorted(list(pd.read_csv(relative_path, sep=sep)))
    a_list.insert(0, "")
    return a_list


def upload_to_drive(gcp_service_account, parent_folder_key, file_name, file_path):
    scope = ['https://www.googleapis.com/auth/drive']
    # credentials = service_account.Credentials.from_service_account_file(filename=path_to_json, scopes=scope)
    credentials = service_account.Credentials.from_service_account_info(
        gcp_service_account, scopes=scope)
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {'name': file_name, 'parents': [parent_folder_key]}
    media = MediaFileUpload(file_path, mimetype='image/png')
    file = service.files().create(body=file_metadata,
                                  media_body=media, fields='id').execute()
    link = '{url}'.format(
        url='https://drive.google.com/open?id=' + file.get('id'))

    return link


def save_uploadedfile(uploadedfile):
    with open(os.path.join("image_cache", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
        path = f'./image_cache/{uploadedfile.name}'
    return path


def clear_image_cache(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
