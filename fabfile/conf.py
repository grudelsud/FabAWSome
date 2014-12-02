import os.path

fabconf = {}

# Username for connecting to EC2 instaces - Do not edit unless you have a reason to
fabconf['SERVER_USERNAME'] = "ubuntu"

#  Do not edit
fabconf['FAB_CONFIG_PATH'] = os.path.dirname(__file__)

# Full local path for .ssh
fabconf['SSH_PATH'] = os.path.join(fabconf['FAB_CONFIG_PATH'], '..', 'secrets')

# Where to install apps
fabconf['APPS_DIR'] = "/home/%s/webapps" % fabconf['SERVER_USERNAME']

# Path for virtualenvs
fabconf['VIRTUALENV_DIR'] = "/home/%s/.virtualenvs" % fabconf['SERVER_USERNAME']



ec2conf = {}

#EC2 region. http://amzn.to/12jBkm7
ec2conf['region'] = ''

# AMI name. http://bit.ly/liLKxj
# ami-00b11177: 14.04 LTS, amd64, ebs
ec2conf['amis'] = []

# Name of the keypair you use in EC2. http://bit.ly/ldw0HZ
ec2conf['keypair'] = ''

# Name of the security group. http://bit.ly/kl0Jyn
ec2conf['secgroups'] = []

# API Name of instance type. http://bit.ly/mkWvpn
ec2conf['instancetype'] = ''


class Configurator(object):
  @classmethod
  def inject_project_conf(cls, project_file):

    # Where you want your project installed: /APPS_DIR/PROJECT_NAME
    fabconf['PROJECT_ROOT'] = "%s/%s" % (fabconf['APPS_DIR'], fabconf['PROJECT_NAME'])

    # Don't edit. Full path of the ssh key you use to connect to EC2 instances
    fabconf['SSH_PRIVATE_KEY_PATH'] = '%s/%s' % (fabconf['SSH_PATH'], fabconf['EC2_KEY_NAME'])

    # Don't edit. Local path for deployment key you use for github
    fabconf['GITHUB_DEPLOY_KEY_PATH'] = "%s/%s" % (fabconf['SSH_PATH'], fabconf['GITHUB_DEPLOY_KEY_NAME'])

    # Where to find manage.py
    fabconf['WSGI_PROJECT_BASE_DIR'] = '%s/%s' % (fabconf['PROJECT_ROOT'], fabconf['DJANGO_PROJECT_PATH'])

    # Creates the ssh location of your GITHUB repo from the above details
    fabconf['GITHUB_REPO'] = "ssh://git@github.com/%s/%s.git" % (fabconf['GITHUB_USERNAME'], fabconf['GITHUB_REPO_NAME'])

    # Virtualenv activate command
    fabconf['ACTIVATE'] = "source /home/%s/.virtualenvs/%s/bin/activate" % (fabconf['SERVER_USERNAME'], fabconf['PROJECT_NAME'])

    # Name tag for your server instance on EC2
    fabconf['INSTANCE_NAME_TAG'] = fabconf['GITHUB_REPO_NAME']

  @classmethod
  def load_project_file(cls, project_name):
    return fabconf, ec2conf
