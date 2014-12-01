# FabAWSome

A bunch of Fabric scripts to manage web stuff on AWS

This fabfile along with the provided templates can spawn EC2 instances, aims at giving a quick and easy way to install, configure and run a variety of services, suchs as a full Django stack (nginx + gunicorn with Amazon S3 for staticfiles) or Varnish caching server.

## Author

[Thomas M. Alisi](https://github.com/grudelsud/)

## Acknowledgements

This is based on [Django-Fabric-AWS](https://github.com/ashokfernandez/Django-Fabric-AWS) by [Ashok Fernandez](https://github.com/ashokfernandez/), his work being inspired [Fabulous](https://github.com/gcollazo/Fabulous) by [Giovanni Collazo](https://github.com/gcollazo).

## Installation
 * create and activate a **virtual environment**
 * cd into the folder and run `pip install -r requirements.txt`

## Configuration

**TODO**

## TODO

- make the plugin structure really pluggable, at the moment it's all entangled with cross-plugin dependencies
- support docker containers as plugin
