# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import pytz
import re
import time

import firebase
from googleapiclient import discovery
import google.auth
import google_auth_httplib2
import requests
import utils

# Set-up logging
logger = utils.get_logger("lights.actuator")


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '18s0N297eQZjQAcXqDeRjDSdlaniIsoW-JTRUU5aW4R8'
RANGE_NAME = 'Sheet1!A2:H4'
TIMEZONE = pytz.timezone("Europe/Madrid")

RE_TIME = re.compile(r"(?P<hours>[0-9][0-9]?):(?P<minutes>[0-9][0-9])")

M_SCHEDULED_TIMER = "scheduled_timer"


def parse_time(time):
    time_obj = None
    if time:
        match = RE_TIME.match(time)
        if match:
            time_obj = datetime.time(int(match.group("hours")), int(match.group("minutes")), tzinfo=TIMEZONE)
    return time_obj


def parse_int(number):
    number_int = None
    if number:
        number_int = int(number)
    return number_int


def is_active(start_time, end_time, current_time):
    active_if_between = False
    active = False
    if start_time is None and end_time is None:
        active = True
    else:
        if start_time is None or end_time is None:
            raise Exception("Missing start or end time")
        if start_time < end_time:
            active_if_between = True
        if ((current_time > start_time and current_time > end_time) or
                (current_time < start_time and current_time < end_time)):
            if not active_if_between:
                active = True
        else:
            if active_if_between:
                active = True
    return active


def get_light(ext_id):
    light = None
    try:
        light = firebase.get_lights().document(ext_id).get()
    except KeyError:
        logger.warning("ext_id [%s] not found", ext_id)
    return light


def actuate(id, channel, new_status):
    url = f"https://shelly-16-eu.shelly.cloud/device/relay/control/"
    req = requests.post(url, data={
        "channel": channel,
        "id": id,
        "auth_key": firebase.get_key(),
        "turn": new_status
    })
    if req.status_code / 200 >= 1 and req.status_code % 200 == 0:
        logger.info("Request sent to Shelly. Returned status code: %s", req.status_code)
    else:
        logger.error("Error while calling Shelly. Status code: [%s]. Response: [%s]", req.status_code, req.json())


def array_get_default(array, index, default):
    return array[index] if index < len(array) else default


def check_lights():
    logger.info("on main()")

    # Get default credentials.
    creds = utils.get_credentials(SCOPES)
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
            id = array_get_default(row, 2, None)
            channel = array_get_default(row, 3, "0")
            mode = array_get_default(row, 4, None)
            start_time = parse_time(array_get_default(row, 5, None))
            end_time = parse_time(array_get_default(row, 6, None))
            timer = parse_int(array_get_default(row, 7, None))
            logger.info("Processing [%s]. Mode: [%s]", name, mode)
            if is_active(start_time, end_time, current_time):
                logger.debug("Rule for [%s] is active", name)
                if mode == M_SCHEDULED_TIMER:
                    light = get_light(ext_id)
                    if light:
                        light_dict = light.to_dict()
                        last_update = light_dict.get(firebase.F_LAST_UPDATE, None)
                        status = light_dict.get(firebase.F_STATUS, None)
                        if status == firebase.STATUS_ON:
                            if time.time() - last_update > timer * 60:
                                logger.info("Time out. Switching off [%s].", name)
                                actuate(id, channel, firebase.STATUS_OFF)
                            else:
                                logger.debug("[%s] is on, but no time out yet.", name)
                    else:
                        logger.info("[%s] not found and timer active. Switching off.")
                        actuate(id, channel, firebase.STATUS_OFF)
        except Exception:
            logger.exception("Exception while processing row %s", i)
        i += 1


if __name__ == "__main__":
    check_lights()
