from .supervisor import Tasks as SupervisorTasks


class Tasks(object):
  mkvirtualenv = SupervisorTasks.stop + [
    {
      "action": "sudo",
      "params": "rm -rf %(VIRTUALENV_DIR)s/%(PROJECT_NAME)s",
      "message": "Cleaning old virtualenv"
    },

    # Create virtual env
    {
      "action": "run",
      "params": "mkvirtualenv --clear --no-site-packages %(PROJECT_NAME)s",
      "message": "creating virtualenv"
    },

    # install gunicorn in virtual env
    {
      "action": "virtualenv",
      "params": "pip install gunicorn",
      "message": "installing gunicorn"
    },
  ]

  update_packages = [
    # Install the requirements from the pip requirements files
    {
    "action": "virtualenv",
    "message": "updating requirements",
    "params": "pip install -r %(WSGI_PROJECT_BASE_DIR)s/requirements/common.txt --upgrade"
    },
  ]

  gunicorn_conf = [
    {
      "action": "put",
      "message": "copy gunicorn configuration file",
      "params":
      {
        "file": "%(FAB_CONFIG_PATH)s/templates/gunicorn.conf.py",
        "destination": "%(WSGI_PROJECT_BASE_DIR)s/gunicorn.conf.py"
      }
    },
  ]

  setup = [
    # Create run and log dirs for the gunicorn socket and logs
    {
      "action": "run",
      "message": "setup logs dir",
      "params": "mkdir -p %(WSGI_PROJECT_BASE_DIR)s/logs"
    },
  ] + mkvirtualenv + update_packages + gunicorn_conf

  django_gunicorn_startup_script = [
    # Add gunicorn startup script to project folder
    {
      "action": "put_template",
      "message": "copy gunicorn startup script",
      "params":
      {
        "template": "%(FAB_CONFIG_PATH)s/templates/gunicorn_start_django.bash",
        "destination": "%(WSGI_PROJECT_BASE_DIR)s/start_gunicorn.bash"
      }
    },
    {
      "action": "sudo",
      "params": "chmod +x %(WSGI_PROJECT_BASE_DIR)s/start_gunicorn.bash"
    },
  ]

  django_setup = setup + django_gunicorn_startup_script + SupervisorTasks.setup

  django_reload = django_setup + SupervisorTasks.restart
