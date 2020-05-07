import logging
import os
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.auth import exceptions as auth_exceptions
import google.cloud.logging

# Set-up logging
logger = logging.getLogger("lights_monitor")
logger.setLevel(logging.INFO)
logger.addHandler(google.cloud.logging.Client().get_default_handler())

# Param names
EXT_ID = 'ext_id'
ACTION = 'action'


def monitor(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    logger.debug('Invoked')
    request_args = request.args
    if EXT_ID in request_args and ACTION in request_args:
        save_new_state(request_args[EXT_ID], request_args[ACTION])
    else:
        logger.warning('Request with no expected arguments: %s', request)
    return "Success"


def save_new_state(ext_id, new_state):
    logger.info('Saving new state. ext_id: [%s], new_state: [%s]', ext_id, new_state)
    # Try to get app. Initialize if app doesn't exist.
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

    db = firestore.client()

    doc_ref = db.collection(u'lights').document(ext_id)
    doc_ref.set({
        u'status': new_state,
        u'lastUpdate': time.time(),
    })
    logger.debug('Finished saving new state')
