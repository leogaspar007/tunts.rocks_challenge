import os.path
import math

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of the spreadsheet.
SPREADSHEET_ID = "1o7a93Aj1BTWockBDKG34zY0L1LmRG88s1JIM3Ei5O4E"


def main():
    """Does the desired calculations and modifications to the spreadsheet."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        main_content = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range="A4:H27")
            .execute()
        )
        number_of_classes_result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range="A2:H2")
            .execute()
        )

        main_content_values = main_content['values']
        number_of_classes = int((str((sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="A2:H2").execute())[
                                'values'][0]).replace("['Total de aulas no semestre: ", "")).replace("']", ""))
        mean = 0
        student_status = []
        for line in main_content_values:
            mean = math.ceil((int(line[3]) + int(line[4]) + int(line[5])) / 3)
            if int(line[2]) > (0.25 * number_of_classes):
                student_status.append(["Reprovado por Falta"])
            else:
                if mean < 50:
                    student_status.append(["Reprovado por Nota"])
                elif 50 <= mean < 70:
                    student_status.append(["Exame final"])
                elif mean >= 70:
                    student_status.append(["Aprovado"])

        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="G4:G27",
                              valueInputOption="USER_ENTERED", body={'values': student_status}).execute()

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
