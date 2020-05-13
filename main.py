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

import actuator
import monitor
import utils

# Set-up logging
logger = utils.get_logger("lights")

# Param names
EXT_ID = 'ext_id'
ACTION = 'action'


def do_monitor(request):
    """Responds to monitor HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    """
    logger.debug('Invoked')
    request_args = request.args
    if EXT_ID not in request_args or ACTION not in request_args:
        raise Exception('Request with no expected arguments: %s', request)
    monitor.save_new_state(request_args[EXT_ID], request_args[ACTION])
    return "Success"


def do_actuator(unused_data, unused_context):
    """Responds to actuate HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    """
    logger.debug('Invoked')
    actuator.check_lights()
    return "Success"

