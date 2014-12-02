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

**WIP**

### EC2

#### Region

http://amzn.to/12jBkm7
`ec2conf['region'] = ''`

#### AMI name

http://bit.ly/liLKxj e.g. ami-00b11177: 14.04 LTS, amd64, ebs
`ec2conf['amis'] = []`

#### Name of the keypair you use in EC2

http://bit.ly/ldw0HZ
`ec2conf['keypair'] = ''`

#### Name of the security group

http://bit.ly/kl0Jyn
`ec2conf['secgroups'] = []`

#### API Name of instance type

http://bit.ly/mkWvpn
`ec2conf['instancetype'] = ''`


## TODO

- make the plugin structure really pluggable, at the moment it's all entangled with cross-plugin dependencies
- support docker containers as plugin
