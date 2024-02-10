import os.path
import math
import config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


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
                config.CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        # Get the main content of the sheet
        main_content_values = (sheet.values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range="A4:H27").execute())['values']

        # Get the total number of classes taught in the semester
        number_of_classes = int((str((sheet.values().get(
            spreadsheetId=config.SPREADSHEET_ID, range="A2:H2").execute())[
            'values'][0]).replace(
            "['Total de aulas no semestre: ", "")).replace("']", ""))

        # Initialize variables
        mean = 0
        student_status = []
        grade_for_approval = []

        # Iterate over the main content list to make the necessary
        # manipulations
        for line in main_content_values:
            mean = math.ceil((int(line[3]) + int(line[4]) + int(line[5])) / 3)

            # Checks if the student has already failed due to missing class
            if int(line[2]) > (0.25 * number_of_classes):
                student_status.append(["Reprovado por Falta"])
                grade_for_approval.append([0])

            # Calculates students' grades to determine their status and how
            # many points they still need to be approved (if aplicable)
            else:
                if mean < 50:
                    student_status.append(["Reprovado por Nota"])
                    grade_for_approval.append([0])
                elif 50 <= mean < 70:
                    student_status.append(["Exame final"])
                    grade_for_approval.append([(100 - mean)])
                elif mean >= 70:
                    student_status.append(["Aprovado"])
                    grade_for_approval.append([0])

        # Updates the spreadsheet with the results found
        sheet.values().update(spreadsheetId=config.SPREADSHEET_ID,
                              range="G4:G27",
                              valueInputOption="USER_ENTERED",
                              body={'values': student_status}).execute()
        sheet.values().update(spreadsheetId=config.SPREADSHEET_ID,
                              range="H4:H27",
                              valueInputOption="USER_ENTERED",
                              body={'values': grade_for_approval}).execute()

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
