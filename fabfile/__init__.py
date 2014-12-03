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
def create_instance(project, type):
  start_time = time.time()

  conf = Configurator(project)
  macro = MacroInterface(conf.get_conf(), conf.get_instance_descriptor(type))
  macro.create_instance()

  print("Instance ready - finished in %.2fs" % (time.time() - start_time))

@task
def webapp_deploy(project, hosts_group):
  conf = Configurator(project)
  hosts = conf.get_hosts_group(hosts_group)
  webapp_deploy_task = tasks['django']['reload']
  command = CommandInterface(conf.get_conf())
  command.run_task(hosts, webapp_deploy_task, 'Deploying webapp', 'Update finished')
