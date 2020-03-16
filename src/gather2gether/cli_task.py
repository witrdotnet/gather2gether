from gather2gether.db.task import *
from gather2gether.cli import print_success, print_fail

import click
from flask.cli import AppGroup
from tabulate import tabulate
import traceback

from gather2gether.db.user import user_find

import logging
logging.disable(logging.INFO)

tasks = AppGroup("tasks")

@tasks.command("create")
@click.argument("project_identifier")
@click.argument("task_number")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
@click.option("--description")
def cli_task_create(project_identifier, task_number, identifier_type, description):
    """Creates new task"""
    try:
        project_identifier_arg = project_identifier
        if identifier_type == "id":
            project_identifier_arg = int(project_identifier)
        task = task_create(project_identifier_arg, task_number, description)
        print_success("Task created successfully")
        print_tasks(task)
    except Exception:
        traceback.print_exc()
        print_fail("Failed to create task")

@tasks.command("find")
@click.argument("project_identifier")
@click.argument("task_number")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
def cli_task_find(project_identifier, task_number, identifier_type):
    """Find task by project name and task number. Returns one task or None"""
    project_identifier_arg = project_identifier
    if identifier_type == "id":
        project_identifier_arg = int(project_identifier)
    task = task_find(project_identifier_arg, task_number)
    if task is None:
        print_success("Not found task with project {0} and task number {1}".format(project_identifier, task_number))
    else:
        print_success("Found task with project {0} and task number {1}".format(project_identifier, task_number))
        print_tasks(task)

@tasks.command("search")
@click.option("--project_name")
@click.option("--task_number")
@click.option("--is_closed", type=bool)
@click.option("--end_date")
@click.option("--date_operator", type=click.Choice(["eq", "lt", "gt", "le", "ge"]))
@click.option("--user_external_id")
def cli_task_search(project_name, task_number, is_closed, end_date, date_operator, user_external_id):
    """Search tasks by criteria. Returns list of tasks"""
    tasks = task_search(project_name, is_closed, task_number, end_date, date_operator, user_external_id)
    print_success("Search properly finished")
    print_tasks(tasks)

@tasks.command("update")
@click.argument("project_identifier")
@click.argument("task_number")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
@click.option("--description")
@click.option("--end_date")
@click.option("--user_external_id")
def cli_task_update(project_identifier, task_number, identifier_type, description, end_date, user_external_id):
    """Updates existing task"""
    try:
        project_identifier_arg = project_identifier
        if identifier_type == "id":
            project_identifier_arg = int(project_identifier)
        user = None
        if user_external_id == "":
            user = ""
        elif not user_external_id is None:
            user = user_find(user_external_id)
        task = task_update(project_identifier_arg, task_number, description, end_date, user)
        print_success("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier))
        print_tasks(task)
    except Exception as e:
        if isinstance(e, Task.DoesNotExist):
            print_fail("Not found task to update, task number: {0} of project: {1}".format(task_number, project_identifier))
        else:
            traceback.print_exc()
            print_fail("Failed to update task, task number: {0} of project: {1}".format(task_number, project_identifier))

@tasks.command("delete")
@click.argument("project_identifier")
@click.argument("task_number")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
def cli_task_delete(project_identifier, task_number, identifier_type):
    """Delete task with provided task number and project name. Returns total deleted tasks"""
    project_identifier_arg = project_identifier
    if identifier_type == "id":
        project_identifier_arg = int(project_identifier)
    try:
        task_delete(project_identifier_arg, task_number)
        print_success("Successfuly deleted task, task number: {0} of project: {1}".format(task_number, project_identifier))
    except Exception:
        traceback.print_exc()
        print_fail("Failed to delete task, task number: {0} of project: {1}".format(task_number, project_identifier))

def print_tasks(tasks):
    headers = ["Task id", "Task number", "Project id", "Project name", "Description", "End date", "User assigned (external_id)"]
    rows = []
    if tasks is None:
        tasks = []
    elif isinstance(tasks, Task):
        tasks = [tasks]
    for task in tasks:
        user_details = None
        if task.user != None:
            user_details = "{} ({})".format(task.user.user_name, task.user.external_id)
        rows.append([task.id, task.task_number, task.project.id, task.project.project_name, task.description, task.end_date, user_details])
    click.secho(tabulate(rows, headers=headers, tablefmt="psql"))
