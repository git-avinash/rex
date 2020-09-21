import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive",
         ]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("FYBSC CS - MeetingLinks").sheet1

sheet_data = sheet.get_all_records()

ml = []

ml.append("🔗")
ml.append("Direct Link")
ml.append("\n")
ml.append("🔐")
ml.append("Classroom Code")
ml.append("\n")

for ml_obj in sheet_data:
    ml.append("\n")
    ml.append("👉")
    ml.append(ml_obj["Time"])
    ml.append("\n")
    ml.append("📕")
    ml.append(ml_obj["Subject"])
    ml.append("\n")
    ml.append("🔗")
    ml.append(ml_obj["Link"])
    ml.append("\n")
    ml.append("🔐")
    ml.append(ml_obj["Code"])
    ml.append("\n")


print(" ".join(ml))
