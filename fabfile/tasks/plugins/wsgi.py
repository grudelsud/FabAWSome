from .supervisor import Tasks as SupervisorTasks


class Tasks(object):
  setup = [
    # Create virtual env
    {
      "action": "run",
      "params": "mkvirtualenv --clear --no-site-packages %(PROJECT_NAME)s",
      "message": "Creating virtualenv"
    },

    # install gunicorn in virtual env
    {
      "action": "virtualenv",
      "params": "pip install gunicorn",
      "message": "Installing gunicorn"
    },

    {
      "action": "put", "params":
      {
        "file": "%(FAB_CONFIG_PATH)s/templates/gunicorn.conf.py",
        "destination": "%(WSGI_PROJECT_BASE_DIR)s/gunicorn.conf.py"
      }
    },

    # Create run and log dirs for the gunicorn socket and logs
    {
      "action": "run",
      "params": "mkdir -p %(WSGI_PROJECT_BASE_DIR)s/logs"
    },
  ]

  template = [
    # Add gunicorn startup script to project folder
    {
      "action": "put_template",
      "params":
        {
          "template": "%(FAB_CONFIG_PATH)s/templates/start_gunicorn.bash",
          "destination": "%(WSGI_PROJECT_BASE_DIR)s/start_gunicorn.bash"
        }
    },
    {
    "action": "sudo",
    "params": "chmod +x %(WSGI_PROJECT_BASE_DIR)s/start_gunicorn.bash"
    },
  ]

  packages = [
    # Install the requirements from the pip requirements files
    {
    "action": "virtualenv",
    "params": "pip install -r %(WSGI_PROJECT_BASE_DIR)s/requirements/common.txt --upgrade"
    },
  ]

  reload = setup + template + packages + SupervisorTasks.restart
