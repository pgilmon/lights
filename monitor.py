import time

import firebase
import utils


# Set-up logging
logger = utils.get_logger("lights.monitor")


def save_new_state(ext_id, new_state):
    logger.info('Saving new state. ext_id: [%s], new_state: [%s]', ext_id, new_state)

    doc_ref = firebase.get_lights().document(ext_id)
    doc_ref.set({
        firebase.F_STATUS: new_state,
        firebase.F_LAST_UPDATE: time.time(),
    })
    logger.debug('Finished saving new state')