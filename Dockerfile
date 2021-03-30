FROM python:3.7-stretch

USER root

RUN mkdir -p '/eh_consumer_workspace'
WORKDIR eh_consumer_workspace
COPY requirements.txt /eh_consumer_workspace
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

WORKDIR async_consumer
ENTRYPOINT [ "python", "azure_event_consumer.py" ]
