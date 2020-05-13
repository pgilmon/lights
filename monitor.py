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