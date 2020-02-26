from gather2gether import app
from gather2gether import g2gServer

from gather2gether.db import g2gDB
from gather2gether.db import init_database
from gather2gether.db.user import *

import click
from flask.cli import AppGroup
from tabulate import tabulate
import traceback

import logging
logging.disable(logging.__all__)

db = AppGroup("db")
tasks = AppGroup("tasks")

@db.command("init")
def cli_init_db():
    """Launch peewee to idempotent initialization of database"""
    init_database(g2gDB)
    print_success("database initialized sucessfully !")

@tasks.command("create")
@click.argument("name")
def cli_task_create(name):
    """Creates new task"""
    print_fail("Under dev.. Coming soon")

def print_success(message):
    click.secho("\n-----------------------------------\nSUCCESS\n-----------------------------------\n{0}\n".format(message), fg="green")

def print_fail(message):
    click.secho("\n-----------------------------------\nFAILED\n-----------------------------------\n{0}\n".format(message), fg="red")
