"""
author : Thomas Alisi (github.com/grudelsud)
credit : Derived from files in https://github.com/ashokfernandez/Django-Fabric-AWS
"""
import time

from conf import Configurator
from tasks import *


# ------------------------------------------------------------------------------------------------------------------
# MAIN FABRIC TASKS - Type fab <function_name> in the command line to execute any one of these
# ------------------------------------------------------------------------------------------------------------------

def create_instance(project, type):
    # Record the starting time and print a starting message
    start_time = time.time()

    # Use boto to create an EC2 instance
    env.host_string = _create_ec2_instance()
    time.sleep(30)

    # Configure the instance that was just created
    # configure()

    # Print out the final runtime and the public dns of the new instance
    end_time = time.time()

def deploy():
    """
    Pulls the latest commit from github, resyncs the database, collects the static files and restarts the
    server.
    """
    _run_task(tasks.deploy, "Updating server to latest commit in the github repo...", "Finished updating the server")

def update_packages():
    """
    Updates the python packages on the server as defined in requirements/common.txt and
    requirements/prod.txt
    """
    _run_task(tasks.update_packages, "Updating server packages with pip...", "Finished updating python packages")

def reload_nginx():
    """
    Reloads the nginx config files and restarts nginx
    """
    _run_task(tasks.reload_nginx, "Reloading the nginx config files...", "Finished reloading nginx")

def reload_supervisor():
    """
    Reloads the supervisor config files and restarts supervisord
    """
    _run_task(tasks.reload_supervisor, "Reloading the supervisor config files...", "Finished reloading supervisor")

def reload_gunicorn():
    """
    Reloads the Gunicorn startup script and restarts gunicorn
    """
    _run_task(tasks.reload_gunicorn, "Reloading the gunicorn startup script...", "Finished reloading the gunicorn startup script")

def manage(command):
    """
    Runs a python manage.py command on the server
    """

    # Get the instances to run commands on
    env.hosts = fabconf['EC2_INSTANCES']

    # Run the management command insite the virtualenv
    _virtualenv("python %(DJANGO_PROJECT_PATH)s/manage.py " + command)

