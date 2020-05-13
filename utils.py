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

import logging

from google.auth import exceptions as auth_exceptions
import google.cloud.logging
from google.oauth2 import service_account


def get_credentials(scopes):
    try:
        creds, project_id = google.auth.default(scopes=scopes)
    except auth_exceptions.DefaultCredentialsError:
        # Use key file if we don't have default credentials.
        creds = service_account.Credentials.from_service_account_file('test_serviceAccount.json').with_scopes(scopes)
    return creds


def get_logger(name):
    logger = logging.getLogger(name)
    try:
        logger.addHandler(google.cloud.logging.Client().get_default_handler())
        logger.setLevel(logging.DEBUG)
    except google.auth.exceptions.DefaultCredentialsError:
        print("Default credentials not found. Using default logging")
        logging.basicConfig(level=logging.INFO)
        logger.setLevel(logging.DEBUG)
    return logger
