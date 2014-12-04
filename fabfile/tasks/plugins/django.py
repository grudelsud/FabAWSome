from .instance import Tasks as InstanceTasks
from .supervisor import Tasks as SupervisorTasks


class Tasks(object):
  # Run npm, bower, collectstatic and syncdb
  compile = [
    {
      "action": "run",
      "params": "cd %(WSGI_PROJECT_BASE_DIR)s && npm install"
    },
    {
      "action": "run",
      "params": "cd %(WSGI_PROJECT_BASE_DIR)s && bower install"
    },
    {
      "action": "virtualenv",
      "params": "python %(WSGI_PROJECT_BASE_DIR)s/manage.py collectstatic -v 0 --noinput --settings='%(DJANGO_SETTINGS_MODULE)s'"
    },
    {
      "action": "virtualenv",
      "params": "python %(WSGI_PROJECT_BASE_DIR)s/manage.py migrate --settings='%(DJANGO_SETTINGS_MODULE)s'"
    },
  ]

  # Pulls the latest commit from the master branch, compile and restart supervisor
  reload = InstanceTasks.pull + compile + SupervisorTasks.restart


class Commands(object):

  manage = {
    "action": "virtualenv",
    "command": "python %(WSGI_PROJECT_BASE_DIR)s/manage.py %s"
  }
