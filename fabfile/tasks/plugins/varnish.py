from .instance import Tasks as InstanceTasks

class Tasks(object):

  install = InstanceTasks.varnish

  setup = [
    {
      "action": "put_template",
      "params":
      {
        "template": "%(FAB_CONFIG_PATH)s/templates/default.vcl",
        "destination": "/home/%(SERVER_USERNAME)s/default.vcl"
      }
    },

    {
      "action": "sudo", "params": "mv /home/%(SERVER_USERNAME)s/default.vcl /etc/varnish/default.vcl"
    },
  ]

  start = [
    {
      "action": "sudo",
      "params": "service varnish start"
    }
  ]

  stop = [
    {
      "action": "sudo",
      "params": "service varnish stop"
    },
  ]

  restart = [
    # Restart gunicorn to update the site
    {
      "action": "sudo",
      "params": "service varnish restart"
    },
  ]

  reload = stop + setup + start
