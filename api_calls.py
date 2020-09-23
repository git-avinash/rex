import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive",
             ]

    # creds.json is not Included in the repo
    # Please create your own key
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1

    timetable_data = sheet.get_all_records()

    return timetable_data
