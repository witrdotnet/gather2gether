from gather2gether import app
from gather2gether import g2gServer
import logging
import click
from flask.cli import AppGroup

from gather2gether.db import g2gDB
from gather2gether.db import init_database
from gather2gether.db.user import *

import logging

logger = logging.getLogger("g2g-cli")

db = AppGroup("db")
tasks = AppGroup("tasks")
users = AppGroup("users")

@db.command("init")
def cli_init_db():
    """Launch peewee to idempotent initialization of database"""
    init_database(g2gDB)
    logger.info("database initialized sucessfully !")


@tasks.command("create")
@click.argument("name")
def cli_task_create(name):
    """Creates new task"""
    logger.info("Under dev.. Coming soon")

@users.command("create")
@click.argument("external_id")
@click.argument("name")
def cli_user_create(external_id, name):
    """Creates new user"""
    user_create(external_id, name)

@users.command("update")
@click.argument("external_id")
@click.option("--name")
@click.option("--active", type=bool)
def cli_user_update(external_id, name, active):
    """Updates existing user"""
    user_update(external_id, name, active)
