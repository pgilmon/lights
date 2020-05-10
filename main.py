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


def do_actuate(request):
    """Responds to actuate HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    """
    logger.debug('Invoked')
    actuator.check_lights()
    return "Success"

