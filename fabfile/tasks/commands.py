def _virtualenv(params):
    """
    Allows running commands on the server
    with an active virtualenv
    """
    with cd(fabconf['APPS_DIR']):
        _virtualenv_command(_render(params))

def _apt(params):
    """
    Runs apt-get install commands
    """
    for pkg in params:
        _sudo("apt-get install -qq %s" % pkg)

def _pip(params):
    """
    Runs pip install commands
    """
    for pkg in params:
        _sudo("pip install %s" % pkg)

def _run(params):
    """
    Runs command with active user
    """
    command = _render(params)
    run(command)

def _sudo(params):
    """
    Run command as root
    """
    command = _render(params)
    sudo(command)

def _put(params):
    """
    Moves a file from local computer to server
    """
    put(_render(params['file']), _render(params['destination']))

def _put_template(params):
    """
    Same as _put() but it loads a file and does variable replacement
    """
    f = open(_render(params['template']), 'r')
    template = f.read()

    run(_write_to(_render(template), _render(params['destination'])))

def _render(template, context=fabconf):
    """
    Does variable replacement
    """
    return template % context

def _write_to(string, path):
    """
    Writes a string to a file on the server
    """
    return "echo '" + string + "' > " + path

def _append_to(string, path):
    """
    Appends to a file on the server
    """
    return "echo '" + string + "' >> " + path

def _virtualenv_command(command):
    """
    Activates virtualenv and runs command
    """
    with cd(fabconf['APPS_DIR']):
        sudo(fabconf['ACTIVATE'] + ' && ' + command, user=fabconf['SERVER_USERNAME'])