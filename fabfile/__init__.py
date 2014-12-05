"""
author : Thomas Alisi (github.com/grudelsud)
credit : Derived from files in https://github.com/ashokfernandez/Django-Fabric-AWS
"""
import time

from fabric.api import task

from tasks import MacroInterface, CommandInterface, tasks
from conf import Configurator

# ------------------------------------------------------------------------------------------------------------------
# MAIN FABRIC TASKS - Type fab <function_name> in the command line to execute any one of these
# ------------------------------------------------------------------------------------------------------------------

@task
def list_plugin_tasks():
  """
  helper function, list plugins+tasks to be used with run_task
  :return:
  """
  for plugin, task_list in tasks.items():
    print '--- %s ---' % (plugin,)
    print task_list.keys()


@task
def run_task(project, instances_group, plugin, task_name):
  """
  call any task by name, params: project, host_group, plugin, task_name

  :param project: what project conf file to use
  :param instances_group: on what group of hosts
  :param plugin:
  :param task_name:
  :return:
  """

  conf = Configurator(project)
  hosts = conf.get_hosts_group(instances_group)

  if tasks.get(plugin, False):

    if plugin == 'django':
      conf.inject_django_conf(instances_group)
    elif plugin == 'varnish':
      conf.inject_varnish_conf(instances_group)

    if tasks[plugin].get(task_name, False):
      CommandInterface.execute(conf.get_conf(),
                               hosts,
                               tasks[plugin][task_name],
                               'Setup instances',
                               'Update finished')
    else:
      print 'task %s is not defined for plugin %s' % (task_name, plugin, )
  else:
    print 'plugin %s is not defined' % (plugin, )


@task
def create_instance(project, instance_type):
  """
  create a fresh instance on EC2, params: project, instance_type (defined in conf)

  :param project:
  :param instance_type:
  :return:
  """
  start_time = time.time()

  conf = Configurator(project)
  macro = MacroInterface(conf.get_conf(), conf.get_instance_descriptor(instance_type))
  macro.create_instance()

  print("Instance ready - finished in %.2fs" % (time.time() - start_time))


@task
def setup_instances(project, instances_group):
  """
  run basic instance initialization, params: project, instances_group (defined in conf)

  :param project:
  :param instances_group:
  :return:
  """
  conf = Configurator(project)
  hosts = conf.get_hosts_group(instances_group)

  CommandInterface.execute(conf.get_conf(),
                           hosts,
                           tasks['instance']['setup'],
                           'Setup instances',
                           'Update finished')

@task
def django_setup(project, instances_group):
  """
  setup supervisor + gunicorn for django, params: project, instances_group

  :param project:
  :param instances_group:
  :return:
  """
  conf = Configurator(project)
  conf.inject_django_conf(instances_group)
  hosts = conf.get_hosts_group(instances_group)

  CommandInterface.execute(conf.get_conf(),
                           hosts,
                           tasks['wsgi']['django_setup'],
                           'Deploying webapp',
                           'Update finished')

@task
def nginx_setup(project, instances_group):
  """
  setup supervisor + gunicorn for django, params: project, instances_group

  :param project:
  :param instances_group:
  :return:
  """
  conf = Configurator(project)
  # TODO: django conf in actuality is only used to define the /static location
  # and potentially can be removed using WSGI_PROJECT_BASE_DIR as base path
  conf.inject_django_conf(instances_group)
  hosts = conf.get_hosts_group(instances_group)

  CommandInterface.execute(conf.get_conf(),
                           hosts,
                           tasks['nginx']['reload'],
                           'Deploying webapp',
                           'Update finished')
@task
def django_deploy(project, instances_group):
  """
  deploy django app, params: project, instances_group

  :param project:
  :param instances_group:
  :return:
  """
  conf = Configurator(project)
  conf.inject_django_conf(instances_group)
  hosts = conf.get_hosts_group(instances_group)

  CommandInterface.execute(conf.get_conf(),
                           hosts,
                           tasks['django']['reload'],
                           'Deploying webapp',
                           'Update finished')
