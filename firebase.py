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

import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.auth import exceptions as auth_exceptions
import utils

# Set-up logging
logger = utils.get_logger("lights.firebase")

F_STATUS = u'status'
F_LAST_UPDATE = u'lastUpdate'

STATUS_ON = "on"
STATUS_OFF = "off"

def get_key():
    return get_firebase_db().collection(u'proteins').document(u'79ns0oYmCQeYOAkMsq5e').get().get('generic')

def get_lights():
    return get_firebase_db().collection(u'lights')


def get_firebase_db():
    try:
        firebase_admin.get_app()
    except ValueError:
        # If app doesn't exist ValueError is raised. Create app.
        cred = credentials.ApplicationDefault()
        try:
            # Next line throws exception if we don't have default credentials.
            cred.get_credential()
            firebase_admin.initialize_app(cred, {
                'projectId': os.environ.get('GCP_PROJECT')
            })
        except auth_exceptions.DefaultCredentialsError:
            # Use key file if we don't have default credentials.
            logger.info('Using key file for credentials')
            cred = credentials.Certificate('test_serviceAccount.json')
            firebase_admin.initialize_app(cred)

    return firestore.client()