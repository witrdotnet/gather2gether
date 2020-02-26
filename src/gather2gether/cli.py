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
users = AppGroup("users")

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

@users.command("create")
@click.argument("external_id")
@click.argument("name")
def cli_user_create(external_id, name):
    """Creates new user"""
    try:
        user = user_create(external_id, name)
        print_success("User created successfully")
        print_users(user)
    except Exception:
        traceback.print_exc()
        print_fail("Failed to create user")

@users.command("find")
@click.argument("external_id")
def cli_user_find(external_id):
    """Find user by its external id. Returns one user or None"""
    user = user_find(external_id)
    if user is None:
        print_success("Not found user with external id {0}".format(external_id))
    else:
        print_success("Found user with external id {0}".format(external_id))
        print_users(user)

@users.command("search")
@click.option("--external_id")
@click.option("--name")
@click.option("--active", type=bool)
def cli_user_search(external_id, name, active):
    """Search users by criteria. Returns list of users"""
    users = user_search(external_id, name, active)
    print_success("Search properly finished")
    print_users(users)

@users.command("update")
@click.argument("external_id")
@click.option("--name")
@click.option("--active", type=bool)
def cli_user_update(external_id, name, active):
    """Updates existing user"""
    try:
        user = user_update(external_id, name, active)
        print_success("Successfuly updated user external id: {0}".format(external_id))
        print_users(user)
    except Exception as e:
        if isinstance(e, User.DoesNotExist):
            print_fail("not found user to update, external id:{0}".format(external_id))
        else:
            traceback.print_exc()
            print_fail("Failed to update user with external_id: {0}".format(external_id))

@users.command("delete")
@click.argument("external_id")
def cli_user_delete(external_id):
    """Delete user with provided external id. Returns total deleted users"""
    user_delete(external_id)
    print_success("Successfuly deleted user external id: {0}".format(external_id))

def print_success(message):
    click.secho("\n-----------------------------------\nSUCCESS\n-----------------------------------\n{0}\n".format(message), fg="green")

def print_fail(message):
    click.secho("\n-----------------------------------\nFAILED\n-----------------------------------\n{0}\n".format(message), fg="red")

def print_users(users):
    headers = ["Externa_id", "Name", "Active"]
    rows = []
    if users is None:
        users = []
    elif isinstance(users, User):
        users = [users]
    for user in users:
        rows.append([user.external_id, user.user_name, user.is_active])
    click.secho(tabulate(rows, headers=headers, tablefmt="psql"))