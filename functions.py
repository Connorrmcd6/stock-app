import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import configs


def write_to_google(df, path_to_json, sheet_key, sheet_name):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(
        path_to_json, scopes=scopes)
    gc = gspread.authorize(credentials)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    # open a google sheet
    gs = gc.open_by_key(sheet_key)

    worksheet = gs.worksheet(sheet_name)

    if len(worksheet.get("A1")) == 0:
        set_with_dataframe(worksheet=worksheet, dataframe=df,
                           include_index=False, include_column_header=True, resize=True)

    else:
        df_values = df.values.tolist()
        gs.values_append(sheet_name, {'valueInputOption': 'RAW'}, {
                         'values': df_values})
