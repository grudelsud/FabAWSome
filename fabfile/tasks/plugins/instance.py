class Tasks(object):
  conf_boto = [
    # Add AWS credentials to the config file so that boto can access S3
    {
      "action": "put_template",
      "params":
      {
        "template": "%(FAB_CONFIG_PATH)s/templates/boto.cfg",
        "destination": "/home/%(SERVER_USERNAME)s/boto.cfg"
      }
    },

    {
      "action": "sudo", "params": "mv /home/%(SERVER_USERNAME)s/boto.cfg /etc/boto.cfg"
    },
  ]

  conf_virtualenvwrapper = [
    # setup virtualenvwrapper
    {
      "action": "sudo",
      "params": "mkdir -p %(VIRTUALENV_DIR)s",
      "message": "Configuring virtualenvwrapper"
    },
    {
      "action": "sudo",
      "params": "chown -R %(SERVER_USERNAME)s: %(VIRTUALENV_DIR)s"
    },
    {
      "action": "run",
      "params": "echo 'export WORKON_HOME=%(VIRTUALENV_DIR)s' >> /home/%(SERVER_USERNAME)s/.profile"
    },
    {
      "action": "run",
      "params": "echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/%(SERVER_USERNAME)s/.profile"
    },
    {
      "action": "run",
      "params": "source /home/%(SERVER_USERNAME)s/.profile"
    },
  ]

  conf_git = [
    # git setup
    {
      "action": "run",
      "params": "git config --global user.name '%(GITHUB_USERNAME)s'",
      "message": "Configuring git"
    },
    {
      "action": "run",
      "params": "git config --global user.email '%(ADMIN_EMAIL)s'"
    },
    {
      "action": "put",
      "params":
      {
        "file": "%(GITHUB_DEPLOY_KEY_PATH)s",
        "destination": "/home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"
      }
    },
    {
      "action": "run",
      "params": "chmod 600 /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"
    },
    {
      "action": "run",
      "params": """echo 'IdentityFile /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s' >> /home/%(SERVER_USERNAME)s/.ssh/config"""
    },
    {
      "action": "run",
      "params": "ssh-keyscan github.com >> /home/%(SERVER_USERNAME)s/.ssh/known_hosts"
    },
  ]

  clone = [
    # Clone the git repo
    {
      "action": "run",
      "params": "rm -rf %(PROJECT_ROOT)s",
      "message": "Cloning git repo"
    },
    {
      "action": "run",
      "params": "git clone %(GITHUB_REPO)s %(PROJECT_ROOT)s"
    },
  ]

  pull = [
    # Pull the latest version from the bitbucket repo
    {
      "action": "run",
      "params": "cd %(PROJECT_ROOT)s && git pull",
      "message": "Pull from git"
    },
  ]

  varnish = [
    {
      "action": "apt",
      "params": ['apt-transport-https']
    },
    {
      "action": "run",
      "params": "curl https://repo.varnish-cache.org/ubuntu/GPG-key.txt | sudo apt-key add -"
    },
    {
      "action": "run",
      "params": "echo 'deb https://repo.varnish-cache.org/ubuntu/ trusty varnish-4.0' | sudo tee -a /etc/apt/sources.list.d/varnish-cache.list"
    },
    {
      "action": "sudo",
      "params": "apt-get update"
    },
    {
      "action": "apt",
      "params": ['varnish']
    },
  ]

  # This takes a few minutes to complete.
  setup = [

    # First command as regular user
    {
      "action": "run",
      "params": "whoami"
    },

    # sudo apt-get update
    {
      "action": "sudo",
      "params": "apt-get update -qq",
      "message": "Updating apt-get"
    },

    # List of APT packages to install
    {
      "action": "apt",
      "params": ["libpq-dev", "nginx", "memcached", "git", "python-setuptools", "python-dev", "build-essential",
                 "python-pip"],
      "message": "Installing apt-get packages"
    },

    # Install additional packages
    {
      "action": "apt",
      "params": ['geoip-bin', 'libgeoip-dev', 'python-geoip', 'libjpeg-dev', 'libjpeg-turbo8-dev', 'nodejs', 'npm'],
      "message": "Installing extra apt-get packages"
    },

    # Setup node with standard packages
    {
      "action": "sudo",
      "params": "ln -s -f /usr/bin/nodejs /usr/bin/node"
    },
    {
      "action": "sudo",
      "params": "chown -R %(SERVER_USERNAME)s /usr/local"
    },
    {
      "action": "run",
      "message": "Installing basic nodejs packages",
      "params": "npm install gulp bower browserify -g"
    },

    # Install standard pypi
    {
      "action": "pip",
      "params": ["virtualenv", "virtualenvwrapper", "supervisor"],
      "message": "Installing pip packages"
    },

    # webapps alias
    {
      "action": "run",
      "params": """echo "alias webapps='cd %(APPS_DIR)s'" >> /home/%(SERVER_USERNAME)s/.profile""",
      "message": "Creating webapps alias"
    },

    # webapps dir
    {
      "action": "sudo",
      "params": "mkdir -p %(APPS_DIR)s",
      "message": "Creating webapps directory"
    },
    {
      "action": "sudo",
      "params": "chown -R %(SERVER_USERNAME)s: %(APPS_DIR)s"
    },

  ] + conf_boto + conf_virtualenvwrapper + conf_git + clone
