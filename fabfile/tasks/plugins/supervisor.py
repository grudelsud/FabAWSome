class Tasks(object):
  # Pushes the supervisor config files to the servers and restarts the supervisor, use this if you
  # have made changes to templates/supervisord-init or templates/supervisord.conf
  setup = [
    {
      "action": "run",
      "params": "echo_supervisord_conf > /home/%(SERVER_USERNAME)s/supervisord.conf",
      "message": "Configuring supervisor"
    },
    {
      "action": "put_template",
      "params":
      {
        "template": "%(FAB_CONFIG_PATH)s/templates/supervisord.conf",
        "destination": "/home/%(SERVER_USERNAME)s/my.supervisord.conf"
      }
    },
    {
      "action": "run",
      "params": "cat /home/%(SERVER_USERNAME)s/my.supervisord.conf >> /home/%(SERVER_USERNAME)s/supervisord.conf"
    },
    {
      "action": "run",
      "params": "rm /home/%(SERVER_USERNAME)s/my.supervisord.conf"
    },
    {
      "action": "sudo",
      "params": "mv /home/%(SERVER_USERNAME)s/supervisord.conf /etc/supervisord.conf"
    },
    {
      "action": "sudo",
      "params": "supervisord"
    },
    {
      "action": "put",
      "params":
      {
        "file": "%(FAB_CONFIG_PATH)s/templates/supervisord-init",
        "destination": "/home/%(SERVER_USERNAME)s/supervisord-init"
      }
    },
    {
      "action": "sudo",
      "params": "mv /home/%(SERVER_USERNAME)s/supervisord-init /etc/init.d/supervisord"
    },
    {
      "action": "sudo",
      "params": "chmod +x /etc/init.d/supervisord"
    },
    {
      "action": "sudo",
      "params": "update-rc.d supervisord defaults"
    },
  ]

  start = [
    {
      "action": "sudo",
      "params": "supervisorctl start all"
    }
  ]

  stop = [
    {
      "action": "sudo",
      "params": "supervisorctl stop all"
    },
    {
      "action": "sudo",
      "params": "killall supervisord"
    },
  ]

  restart = [
    # Restart gunicorn to update the site
    {
      "action": "sudo",
      "params": "supervisorctl restart %(PROJECT_NAME)s"
    },
  ]

  reload = stop + setup + start
