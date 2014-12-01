# FabAWSome

A bunch of Fabric scripts to manage web stuff on AWS

This fabfile along with the provided templates can spawn EC2 instances, aims at giving a quick and easy way to install, configure and run a variety of services, suchs as a full Django stack (nginx + gunicorn with Amazon S3 for staticfiles) or Varnish caching server.

## Author

[Thomas M. Alisi](https://github.com/grudelsud/)

## Acknowledgements

This is based on [Django-Fabric-AWS](https://github.com/ashokfernandez/Django-Fabric-AWS) by [Ashok Fernandez](https://github.com/ashokfernandez/), and his work being inspired [Fabulous](https://github.com/gcollazo/Fabulous) by [Giovanni Collazo](https://github.com/gcollazo).

## Installation
 * create and activate a **virtual environment**
 * cd into the folder and run `pip install -r requirements.txt`

## Configuration

### Existing instances

defined in to project.json, used to add the public dns of your instances grouped by families after you have spawned them

`fabconf['EC2_INSTANCES'] = {'family': ['']}`

### Project name 

defined in project.json

`fabconf['PROJECT_NAME'] = ""`

### EC2 Key

defined in project.json, name of the private key file you use to connect to EC2 instances (located in the secrets folder) 

`fabconf['EC2_KEY_NAME'] = ''`

### Email for the server admin 

defined in project.json

`fabconf['ADMIN_EMAIL'] = "webmaster@yourdomain.com"`

### Git username for the server 

defined in project.json

`fabconf['GIT_USERNAME'] = ""`

### Github deploy key

defined in project.json, name of the private key file used for github deployments 

`fabconf['GITHUB_DEPLOY_KEY_NAME'] = ""`

### Github user/repo 

defined in project.json, used to derive full path to the repo of the application you want to install 

  fabconf['GITHUB_USERNAME'] = 'Stinkdigital'
  fabconf['GITHUB_REPO_NAME'] = 'Warp-Records'

### EC2 key

defined in project.json, [check this out](http://bit.ly/j5ImEZ)

`fabconf['AWS_ACCESS_KEY'] = ''`

### EC2 secret

defined in project.json, [check this out](http://bit.ly/j5ImEZ)

`fabconf['AWS_SECRET_KEY'] = ''`

### App domains 

defined in project.json, what domains NGINX should listen for

`fabconf['DOMAINS'] = ""`

### Django Specific

defined in project.json, Django project name

`fabconf['DJANGO_PROJECT_NAME'] = ''`

defined in project.json, where to find manage.py relative to `PROJECT_ROOT` (automatically detected)

# fabconf['DJANGO_PROJECT_PATH'] = 'www/%s' % (fabconf['DJANGO_PROJECT_NAME'],)
 
defined in project.json, Django settings file

`fabconf['DJANGO_SETTINGS_MODULE'] = "%s.settings.bla" % (fabconf['DJANGO_PROJECT_NAME'],)`

## TODO

- make the plugin structure really pluggable, at the moment it's all entangled with cross-plugin dependencies
- support docker containers as plugin
