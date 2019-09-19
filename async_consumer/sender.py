'''
Module to send enriched logs to graylog.
'''

import json
import logging
import socket
from ehc_config import CONFIG_DICT, ACTIVE_ENV

LOGGER = logging.getLogger(__name__)
CONFIG = CONFIG_DICT[ACTIVE_ENV]
# GrayLog initialization
GRAYLOG_IP = CONFIG.GRAYLOG_IP
GRAYLOG_PORT = CONFIG.GRAYLOG_PORT


def enrich_and_send(actual_data):
    '''
    Based on operation name enrich and send logs to graylog.
    '''
    azure_logs = {}
    consumer_host = socket.gethostname()
    short_msg_host_field = {"host": consumer_host}
    azure_logs.update(short_msg_host_field)

    for _, record in enumerate(actual_data['records']):
        azure_logs.update({"short_message": record.get(
            'operationName', 'operationNameNotFound')})
        azure_logs.update(record)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
                socket_obj.settimeout(3)
                socket_obj.connect((GRAYLOG_IP, GRAYLOG_PORT))
                socket_obj.send(json.dumps(azure_logs).encode('utf-8'))
                socket_obj.send(b'\0')
        except Exception as e_msg:
            LOGGER.error("Exception while sending to graylog: %s", e_msg)
            return "Error"

    return None
