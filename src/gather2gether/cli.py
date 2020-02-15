from gather2gether import app
from gather2gether import g2gServer
import logging
import click
from flask.cli import AppGroup

tasks = AppGroup('tasks')
users = AppGroup('users')

@tasks.command("create")
@click.argument("name")
def create_task(name):
    """Creates new task"""
    logger = logging.getLogger('g2g-cli')
    logger.info('Under dev.. Coming soon')

@users.command("create")
@click.argument("name")
def create_user(name):
    """Creates new user"""
    logger = logging.getLogger('g2g-cli')
    logger.info('Under dev.. Coming soon')