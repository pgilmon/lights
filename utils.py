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
