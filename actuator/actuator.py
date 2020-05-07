import logging

from googleapiclient import discovery
import google.auth
import google_auth_httplib2
import google.cloud.logging

# Set-up logging
logger = logging.getLogger("lights_actuator")
logger.setLevel(logging.INFO)
logger.addHandler(google.cloud.logging.Client().get_default_handler())


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '18s0N297eQZjQAcXqDeRjDSdlaniIsoW-JTRUU5aW4R8'
RANGE_NAME = 'Sheet1!B1:G4'


def main(request):
    logger.info("on main()")

    # Get default credentials.
    creds = google.auth.default(scopes=SCOPES)
    http = google_auth_httplib2.AuthorizedHttp(creds)
    service = discovery.build('sheets', 'v4', http=http)

    # Get values from sheets API.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        logging.error('No values.')
    else:
        logging.info('Values')
        i = 1
        j = 1
        for row in values:
            for element in row:
                logging.info('(%s,%s): %s', i, j, element)
    logging.info('Finished.')

