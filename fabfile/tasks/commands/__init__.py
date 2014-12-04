import time

import boto.ec2
from fabric.api import env, execute, run, sudo, put, cd
from fabric.colors import cyan, magenta, yellow, green


class MacroInterface(object):
  def __init__(self, conf, ec2conf):
    self.conf = conf
    self.ec2conf = ec2conf

    if not ec2conf:
      raise BaseException('wrong type for EC2_INSTANCE_TYPES specified when calling this function')

  def create_instance(self):
    print(cyan("Creating instance"))
    aws_key = {
      'aws_access_key_id': self.conf['AWS_ACCESS_KEY'],
      'aws_secret_access_key': self.conf['AWS_SECRET_KEY']
    }
    conn = boto.ec2.connect_to_region(self.ec2conf['region'], **aws_key)
    image = conn.get_all_images(self.ec2conf['amis'])

    reservation = image[0].run(1, 1,
                               self.ec2conf['keypair'],
                               self.ec2conf['secgroups'],
                               instance_type=self.ec2conf['instancetype'])

    instance = reservation.instances[0]
    conn.create_tags([instance.id], {"Name": self.conf['INSTANCE_NAME_TAG']})

    while instance.state == u'pending':
      print(yellow("Instance state: %s. Will check again in 10 seconds" % instance.state))
      time.sleep(10)
      instance.update()

    print(green("Instance state: %s" % instance.state))
    print(cyan("Public DNS: %s [add this to your EC2_INSTANCES group in conf.json]" % instance.public_dns_name))

    return instance.public_dns_name


class CommandInterface(object):
  def __init__(self, conf):
    self.conf = conf

    # AWS user credentials
    env.user = conf['SERVER_USERNAME']
    env.key_filename = conf['SSH_PRIVATE_KEY_PATH']

  def execute(self, hosts, task, start_message, finished_message):
    print(cyan(start_message))
    start_time = time.time()

    execute(self._run_task, task, hosts=hosts)

    print(green("%s in %.2fs" % (finished_message, time.time() - start_time)))

  def _run_task(self, task):

    # Run the task items
    for item in task:
      try:
        print(yellow(item['message']))
      except KeyError:
        pass

      try:
        f = getattr(self, '_%s' % (item['action'], ))
        f(item['params'])
      except AttributeError as e:
        print(magenta('error while executing task: %s' % (e, )))


  def _run(self, params):
    """
    Runs command with active user
    """
    command = self._render(params)
    run(command)

  def _sudo(self, params):
    """
    Run command as root
    """
    command = self._render(params)
    sudo(command)

  def _render(self, template, context=None):
    """
    Does variable replacement
    """
    if not context:
      context = self.conf

    return template % context

  def _apt(self, params):
    """
    Runs apt-get install commands
    """
    for pkg in params:
      self._sudo("apt-get install -qq %s" % pkg)

  def _pip(self, params):
    """
    Runs pip install commands
    """
    for pkg in params:
      self._sudo("pip install %s" % pkg)

  def _put(self, params):
    """
    Moves a file from local computer to server
    """
    put(self._render(params['file']), self._render(params['destination']))

  def _put_template(self, params):
    """
    Same as _put() but it loads a file and does variable replacement
    """
    f = open(self._render(params['template']), 'r')
    template = f.read()

    run(self._write_to(self._render(template), self._render(params['destination'])))

  def _write_to(self, string, path):
    """
    Writes a string to a file on the server
    """
    return "echo '" + string + "' > " + path

  def _append_to(self, string, path):
    """
    Appends to a file on the server
    """
    return "echo '" + string + "' >> " + path

  def _virtualenv(self, params):
    """
    Allows running commands on the server
    with an active virtualenv
    """
    with cd(self.conf['APPS_DIR']):
      self._virtualenv_command(self._render(params))

  def _virtualenv_command(self, command):
    """
    Activates virtualenv and runs command
    """
    with cd(self.conf['APPS_DIR']):
      sudo(self.conf['ACTIVATE'] + ' && ' + command, user=self.conf['SERVER_USERNAME'])

