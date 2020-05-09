import datetime
import logging
import pytz
import re

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
RANGE_NAME = 'Sheet1!A1:G4'
TIMEZONE = pytz.timezone("Europe/Madrid")

RE_TIME = re.compile(r"(?P<hours>[0-9][0-9]?):(?P<minutes>[0-9][0-9])")

M_SCHEDULED_TIMER = "scheduled_timer"

def parse_time(time):
    match = RE_TIME.match(time)
    time_obj = None
    if match:
        time_obj = datetime.time(int(match.group("hours")), int(match.group("minutes")), tzinfo=TIMEZONE)
    return time_obj

def parse_int(number):
    number_int = None
    if number:
        number_int = int(number)
    return number_int

def actuator(request):
    logger.info("on main()")

    # Get default credentials.
    creds, project_id = google.auth.default(scopes=SCOPES)
    http = google_auth_httplib2.AuthorizedHttp(creds)
    service = discovery.build('sheets', 'v4', http=http, cache_discovery=False)

    # Get values from sheets API.
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    current_time = datetime.datetime.now(tz=TIMEZONE).timetz()

    if not values:
        raise Exception("No configuration found on spreadsheet ID %s" % SPREADSHEET_ID)
    i = 0
    for row in values:
        try:
            name = row[0]
            ext_id = row[1]
            id = row[2]
            mode = row[3]
            start_time = parse_time(row[4])
            end_time = parse_time(row[5])
            timer = parse_int(row[6])
            logging.info("Processing [%s]. Mode: [%s]", name, mode)
            if mode == M_SCHEDULED_TIMER:
                



        except Exception:
            logger.error("Exception while processing row %s", i)



    logging.info('Finished.')

