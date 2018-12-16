# worker_images
[![Build Status](https://travis-ci.org/Youkoulayley/worker_images.svg?branch=master)](https://travis-ci.org/Youkoulayley/worker_images)
[![Coverage Status](https://coveralls.io/repos/github/Youkoulayley/worker_images/badge.svg?branch=master)](https://coveralls.io/github/Youkoulayley/worker_images?branch=master)

This project aims to manage the images of the Série-All website. But the project has been thinking with idea 
of being adapted to any other usages.
The worker images takes message from NATS, download the desired image, resize it and crop if necessary.

**Workflow of the worker** :

![Worflow](worflow/workflow.jpg)

## NATS
A NATS streaming server is mandatory for the functioning of the worker_images.
The message send to the worker image need to have this format : 

```json
{
  "url": "https://www.thetvdb.com/banners/fanart/original/5b0fcf2c5c1b5.jpg", 
  "name": "supergirl", 
  "crop_type": "poster", 
  "crop": "middle",
  "force_crop": "false"
}
```

The message contains different section :

* **URL**: The URL where to download the image ;
* **Name**: The name of the image when saved to the disk ;
* **Crop_type**: The type to use (show config.ini for more informations) ;
* **Crop**: The alignment of the crop ;
* **Force_crop**: If true, force the resize & crop, even if the fil exists.

## Arguments
You can pass a config file in parameter to launch the application :
```
usage: worker_images [-h] -c CONFIG_FILE

Worker images resize & crop image.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Provide config file for the application
```

## config.ini
Example : 

```
[DEFAULT]
images_folder = ../images
original_folder = %(images_folder)s/original
image_formats = {
    "poster": [
        "200_200",
        "300_300",
        "500_150"
        ],
    "banner": [
        "100_50"
    ]}

[LOGGING]
level = debug

[NATS]
servers = ["nats://127.0.0.1:4222"]
tls = no
ca_cert = /etc/ssl/nats/ca.pem
client_cert = /etc/ssl/nats/client_cert.pem
client_key = /etc/ssl/nats/client_cert.key
cluster_id = serieall
connection_name = worker_images
channel = worker_images
```

The Default section contains the configuration for the application.

|Name|Description|Type|
|----|-----------|----|
|images_folder|Path of images folder|path|
|original_folder|Path of originals images|path|
|image_formats|A list of format to crop divided by type. Each type can have a different set of formats. You have to precise the type in the message sent to NATS|list|

The Logging section contains the configuration for the logger.

|Name|Description|Type|
|----|-----------|----|
|level|Log Level|debug/info/warning/error|

The NATS section contains the configuration to connect to NATS

|Name|Description|Type|
|----|-----------|----|
|servers|List of NATS server to connect to|list|
|tls|Is the connection to NATS server needs TLS ?|yes/no|
|ca_cert|The CA cert to connect to NATS server|string|
|client_cert|The client cert to connect to NATS server|string|
|client_key|The client key to connect to NATS server|string|
|cluster_id|The cluster of the NATS server|string|
|connection_name|The name of the application, used for the connection to NATS|string|
|channel|Channel where the NATS messages are send|string|

## Development
Before starting to contribute to this project, you need to setup a NATS Streaming Server. A docker-compose file is present at the root of the repo for this purpose.
Just launch it : 
```bash
docker-compose up -d
``` 

Yo can test sending a message to NATS with the bin/nats_pub.py script.

## Tests
The project has unit tests and you need to pass all of them before your PR is validated.
Just run :
```bash 
make unittests
```

## Contributing

Thanks for thinking about contributing to worker_images! The success of an open source project is entirely down to the efforts of its contributors, so thank you for even thinking of contributing.

Before you do so, you should check out our contributing guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file, to make sure it's as easy as possible for us to accept your contribution.