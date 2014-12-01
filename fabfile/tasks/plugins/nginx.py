# Pushes the nginx config files to the servers and restarts the nginx, use this if you 
# have made changes to templates/nginx-app-proxy or templates/nginx.conf

setup = [
  {
    "action":"put", 
    "params":{
      "file":"%(FAB_CONFIG_PATH)s/templates/nginx.conf",
      "destination":"/home/%(SERVER_USERNAME)s/nginx.conf"
    },
    "message":"Configuring nginx"
  },
  {
    "action":"sudo", 
    "params":"mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old"
  },
  {
    "action":"sudo", 
    "params":"mv /home/%(SERVER_USERNAME)s/nginx.conf /etc/nginx/nginx.conf"
  },
  {
    "action":"sudo", 
    "params":"chown root:root /etc/nginx/nginx.conf"
  },
  {
    "action":"put_template", 
    "params":
    {
      "template":"%(FAB_CONFIG_PATH)s/templates/nginx-app-proxy",
      "destination":"/home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s"
    }
  },
  {
    "action":"sudo", 
    "params":"rm -rf /etc/nginx/sites-enabled/default"
  },
  {
    "action":"sudo", 
    "params":"mv /home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s /etc/nginx/sites-available/%(PROJECT_NAME)s"
  },
  {
    "action":"sudo", 
    "params":"ln -s -f /etc/nginx/sites-available/%(PROJECT_NAME)s /etc/nginx/sites-enabled/%(PROJECT_NAME)s"
  },
  {
    "action":"sudo", 
    "params":"chown root:root /etc/nginx/sites-available/%(PROJECT_NAME)s"
  },
  {
    "action":"sudo", 
    "params":"/etc/init.d/nginx restart", 
    "message":"Restarting nginx"
  },
]

stop = [
  {
    "action":"sudo", 
    "params":"service nginx stop"
  },
]

start = [
  {
    "action":"sudo", 
    "params":"/etc/init.d/nginx restart", 
    "message":"Restarting nginx"
  },
]

restart = start

reload = stop + setup + start
