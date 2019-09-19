'''
This module will fetch logs from azure event hub
consumer. To run this module we must have
shared access key and consumer group of azure event hub.
'''

import os
import asyncio
import logging.config
import logging
import sys
import yaml

from azure.eventhub import EventHubClient as ehub_client
from azure.eventhub.aio import EventHubClient
from azure.eventhub import EventPosition, EventHubSharedKeyCredential

from sender import enrich_and_send
from ehc_config import ACTIVE_ENV, CONFIG_DICT

LOGGER = logging.getLogger(__name__)

CONFIG = CONFIG_DICT[ACTIVE_ENV]
EVENT_POSITION = EventPosition("@latest")
# EVENT_POSITION = EventPosition("-1")


def setup_logging(default_path, default_level=logging.INFO):
    '''
    Setting up logging for Azure event hub consumer.
    '''

    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f_log:
            log_config = yaml.safe_load(f_log.read())
            logging.config.dictConfig(log_config)
    else:
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s:%(levelname)s:%(message)s"
        )

EH_NAME = CONFIG.EVENT_HUB
os.makedirs("event-hubs" + "/" + EH_NAME, exist_ok=True)
EH_STORE_PATH = "event-hubs" + "/" + EH_NAME


def get_eh_partition_id():
    '''
    Get the number of partition in eventhub.
    '''
    client = ehub_client.from_connection_string(CONFIG.CONNECTION_STRING)
    partition_ids = client.get_partition_ids()
    return partition_ids


async def pump(client, partition, data_position):
    '''
    It will receive the Azure events and after enriching the log
    send to Graylog GELF TCP Input.
    '''
    consumer = client.create_consumer(
        consumer_group=CONFIG.CONSUMER_GROUP,
        partition_id=partition,
        event_position=data_position,
        prefetch=500)
    async with consumer:
        while True:
            batch = await consumer.receive(timeout=10)
            for event_data in batch:
                try:
                    last_offset = event_data.offset
                    last_sn = event_data.sequence_number
                    log_msg = "Received: Offset: {}, sequence_no: {},partition: {},data: {}".format(
                        last_offset, last_sn,
                        partition,
                        event_data.body_as_str())
                    LOGGER.info(log_msg)

                    actual_data = event_data.body_as_json()
                    if 'records' not in actual_data:
                        raise ValueError
                    res = enrich_and_send(actual_data)
                    if res is not None:
                        LOGGER.error("stopping loop")
                        sys.exit(1)
                    partition_file_name = EH_STORE_PATH + \
                        "/partition_{}".format(partition)
                    with open(partition_file_name, "w") as f_offset:
                        f_offset.write(last_offset)
                except ValueError:
                    LOGGER.info(
                        "Records not found in data. Not a valid Azure activity log.")
                except Exception as e_msg:
                    LOGGER.info(e_msg)


if __name__ == '__main__':
    LOG_CONFIGFILE = os.path.join(os.getcwd(), 'log_config.yaml')
    setup_logging(default_path=LOG_CONFIGFILE)

    try:
        LOOP = asyncio.get_event_loop()
        CLIENT = EventHubClient(
            host=CONFIG.HOSTNAME,
            event_hub_path=CONFIG.EVENT_HUB,
            credential=EventHubSharedKeyCredential(
                CONFIG.USER, CONFIG.KEY),
            network_tracing=False)
        TASKS = []
        for part_id in get_eh_partition_id():
            eh_partition_fname = EH_STORE_PATH + \
                "/partition_{}".format(part_id)
            if os.path.exists(eh_partition_fname):
                with open(eh_partition_fname, "r") as f:
                    last_offset_no = f.readlines()[0].strip()
                    event_position = EventPosition(str(last_offset_no))
                    TASKS.append(asyncio.ensure_future(
                        pump(CLIENT, str(part_id), event_position)))
            else:
                TASKS.append(asyncio.ensure_future(
                    pump(CLIENT, str(part_id), EVENT_POSITION)))
        LOOP.run_until_complete(asyncio.wait(TASKS))
    except Exception as e_msg:
        LOGGER.error(e_msg)
    finally:
        LOOP.close()
