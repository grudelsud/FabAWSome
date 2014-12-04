from .instance import Tasks as InstanceTasks
from .supervisor import Tasks as SupervisorTasks
from .wsgi import Tasks as WSGITasks

class Tasks(object):

  update_packages = WSGITasks.update_packages

  node_packages = [
    {
      "action": "run",
      "message": "npm + bower install",
      "params": "cd %(WSGI_PROJECT_BASE_DIR)s && npm install"
    },
    {
      "action": "run",
      "params": "cd %(WSGI_PROJECT_BASE_DIR)s && bower install"
    },
  ]

  collectstatic = [
    {
      "action": "virtualenv",
      "message": "collect django static files",
      "params": "python %(WSGI_PROJECT_BASE_DIR)s/manage.py collectstatic -v 0 --noinput --settings='%(DJANGO_SETTINGS_MODULE)s'"
    },
  ]

  migrate = [
    {
      "action": "virtualenv",
      "message": "migrate db",
      "params": "python %(WSGI_PROJECT_BASE_DIR)s/manage.py migrate --settings='%(DJANGO_SETTINGS_MODULE)s'"
    },
  ]

  compile = node_packages + collectstatic + migrate

  setup_supervisor = SupervisorTasks.setup

  # Pulls the latest commit from the master branch, compile and restart supervisor
  reload = InstanceTasks.pull + compile + SupervisorTasks.restart


class Commands(object):

  manage = {
    "action": "virtualenv",
    "command": "python %(WSGI_PROJECT_BASE_DIR)s/manage.py %s"
  }
