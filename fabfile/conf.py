import os.path
import json
import re

DEFAULT_USERNAME = 'ubuntu'
DEFAULT_PATH = os.path.dirname(__file__)


class Configurator(object):

  def __init__(self, project_name):

    self.conf = {
      'SERVER_USERNAME': DEFAULT_USERNAME,
      'FAB_CONFIG_PATH': DEFAULT_PATH,
      'SSH_PATH': os.path.join(DEFAULT_PATH, '..', 'secrets'),
      'APPS_DIR': "/home/%s/webapps" % DEFAULT_USERNAME,
      'VIRTUALENV_DIR': "/home/%s/.virtualenvs" % DEFAULT_USERNAME,
    }

    project_file = os.path.join(DEFAULT_PATH, '..', 'projects', '%s.json' % (project_name, ))

    if os.path.isfile(project_file):
      with open(project_file, 'r') as f:
        project_conf = json.load(f)
        self._inject_project_conf(project_conf)
    else:
      raise BaseException('project file does not exist at search path %s' % project_file)

  def _inject_project_conf(self, project_conf):

    self.conf.update(project_conf)

    # Where you want your project installed: /APPS_DIR/PROJECT_NAME
    self.conf['PROJECT_ROOT'] = "%s/%s" % (self.conf['APPS_DIR'], project_conf['PROJECT_NAME'])

    # Don't edit. Full path of the ssh key you use to connect to EC2 instances
    self.conf['SSH_PRIVATE_KEY_PATH'] = '%s/%s' % (self.conf['SSH_PATH'], project_conf['EC2_KEY_NAME'])

    # Don't edit. Local path for deployment key you use for github
    self.conf['GITHUB_DEPLOY_KEY_PATH'] = "%s/%s" % (self.conf['SSH_PATH'], project_conf['GITHUB_DEPLOY_KEY_NAME'])

    # Creates the ssh location of your GITHUB repo from the above details
    self.conf['GITHUB_REPO'] = "ssh://git@github.com/%s/%s.git" % (project_conf['GITHUB_USERNAME'], project_conf['GITHUB_REPO_NAME'])

    # Virtualenv activate command
    self.conf['ACTIVATE'] = "source /home/%s/.virtualenvs/%s/bin/activate" % (self.conf['SERVER_USERNAME'], project_conf['PROJECT_NAME'])

    # Name tag for your server instance on EC2
    self.conf['INSTANCE_NAME_TAG'] = project_conf['PROJECT_NAME']

  def inject_django_conf(self, environment):
    if re.search(r'django', self.conf['PROJECT_CONFIGURATION']['TYPE'], re.IGNORECASE):
      data = dict(self.conf['PROJECT_CONFIGURATION']['DETAILS'])
      data['WSGI_PROJECT_BASE_DIR'] = '%s/%s' % (self.conf['PROJECT_ROOT'], data['DJANGO_PROJECT_PATH'])
      data.update(self.conf['PROJECT_CONFIGURATION']['ENVIRONMENT'][environment])
      self.conf.update(data)

  def get_conf(self):
    return self.conf

  def get_instance_descriptor(self, instance_type):
    return self.conf['EC2_INSTANCE_TYPES'].get(instance_type, None)

  def get_hosts_group(self, group_name):
    return self.conf['EC2_INSTANCES'].get(group_name, None)
