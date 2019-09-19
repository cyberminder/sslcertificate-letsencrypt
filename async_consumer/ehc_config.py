'''
Configuration file for Event hub consumer.
'''


class BaseConfig:
    '''
    Base config for all environments
    '''
    pass


class LocalConfig(BaseConfig):
    '''
    Local configuration.
    '''
    EVENTHUB_NAMESPACE = 'YOUR_NAMESPACE'
    EVENT_HUB = 'EVENT_HUB'  # Fixed
    USER = 'KEY_NAME'  # Shared access policy name
    # Shared access policy primary key
    KEY = 'lkdnfew7844runfkjensfkey+yyw/XWB8Dupo='
    CONSUMER_GROUP = "CONSUMER_GROUP"

    HOSTNAME = '{}.servicebus.windows.net'.format(EVENTHUB_NAMESPACE)
    CONNECTION_STRING = "Endpoint=sb://{}.servicebus.windows.net/;" \
        "SharedAccessKeyName={};SharedAccessKey={};EntityPath={}".format(
            EVENTHUB_NAMESPACE, USER, KEY, EVENT_HUB)

    # GrayLog GELF TCP input IP and Port.
    GRAYLOG_IP = '192.168.56.101'
    GRAYLOG_PORT = 12201


class DevelopmentConfig(BaseConfig):
    '''
    Dev Configuration.
    '''
    EVENTHUB_NAMESPACE = 'YOUR_NAMESPACE'
    EVENT_HUB = 'EVENT_HUB'  # Fixed
    USER = 'KEY_NAME'  # Shared access policy name
    # Shared access policy primary key
    KEY = 'lkdnfew7844runfkjensfkey+yyw/XWB8Dupo='
    CONSUMER_GROUP = "CONSUMER_GROUP"

    HOSTNAME = '{}.servicebus.windows.net'.format(EVENTHUB_NAMESPACE)
    CONNECTION_STRING = "Endpoint=sb://{}.servicebus.windows.net/;" \
        "SharedAccessKeyName={};SharedAccessKey={};EntityPath={}".format(
            EVENTHUB_NAMESPACE, USER, KEY, EVENT_HUB)

    # GrayLog GELF TCP input IP and Port.
    GRAYLOG_IP = '192.168.56.101'
    GRAYLOG_PORT = 12201


class TestingConfig(BaseConfig):
    '''
    Test configuration.
    '''
    EVENTHUB_NAMESPACE = 'YOUR_NAMESPACE'
    EVENT_HUB = 'EVENT_HUB'  # Fixed
    USER = 'KEY_NAME'  # Shared access policy name
    # Shared access policy primary key
    KEY = 'lkdnfew7844runfkjensfkey+yyw/XWB8Dupo='
    CONSUMER_GROUP = "CONSUMER_GROUP"

    HOSTNAME = '{}.servicebus.windows.net'.format(EVENTHUB_NAMESPACE)
    CONNECTION_STRING = "Endpoint=sb://{}.servicebus.windows.net/;" \
        "SharedAccessKeyName={};SharedAccessKey={};EntityPath={}".format(
            EVENTHUB_NAMESPACE, USER, KEY, EVENT_HUB)

    # GrayLog GELF TCP input IP and Port.
    GRAYLOG_IP = '192.168.56.101'
    GRAYLOG_PORT = 12201


CONFIG_DICT = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'test': TestingConfig,
}

ACTIVE_ENV = 'local'
