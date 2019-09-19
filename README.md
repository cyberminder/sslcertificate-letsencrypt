## Event Hub consumer script

### This script consumes events from Azure Event Hubs, a highly scalable data streaming platform and event ingetion service.

Many Azure services integrate with the Azure Events Hubs. Azure Monitor, for example, integrates with Azure Event Hubs to provide infrastructure metrics.

* Its a simple consumer which get logs from Azure eventhub and send it to Graylog.
  - Create a GELF TCP input in Graylog.
  - Configure Graylog GELF TCP input ip and port in config file.
  - By default active env is local in config file you can keep your credentials as u wish.

* To run the script:
  - Create virtualenv
  - Install required packages. `pip install -r requirements.txt`
  - `cd async_consumer && python azure_event_consumer.py`
  - You can check the logs in Graylog.


## How to run this script in Docker container.
* clone this repository.
* Go to repo folder and build docker image `docker build -t ehconsumer .`
* Find the path of cloned repo and pass it in next step as local_path e.g. if cloned in /opt then local path will be /opt/ azure-eventhub-consumer.
* Run script in a container `docker run -d --name ehc -v <local_path>:/eh_consumer_workspace ehconsumer`

## Check script logs.
To check container logs `docker logs ehc`
