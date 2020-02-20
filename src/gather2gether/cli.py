from gather2gether import app
from gather2gether import g2gServer
import logging
import click
from flask.cli import AppGroup
from gather2gether.db import g2gDB
from gather2gether.db import init_database
import logging

logger = logging.getLogger("g2g-cli")

db = AppGroup('db')
tasks = AppGroup('tasks')
users = AppGroup('users')

@db.command("init")
def init_db():
    """Launch peewee to idempotent initialization of database"""
    init_database(g2gDB)
    logger.info('database initialized sucessfully !')


@tasks.command("create")
@click.argument("name")
def create_task(name):
    """Creates new task"""
    logger.info('Under dev.. Coming soon')

@users.command("create")
@click.argument("name")
def create_user(name):
    """Creates new user"""
    logger.info('Under dev.. Coming soon')