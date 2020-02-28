from gather2gether.db.task import *
from gather2gether.cli import print_success, print_fail

import click
from flask.cli import AppGroup
from tabulate import tabulate
import traceback

from gather2gether.db.user import user_find

import logging
logging.disable(logging.__all__)

tasks = AppGroup("tasks")

@tasks.command("create")
@click.argument("project_name")
@click.argument("task_number")
@click.option("--description")
def cli_task_create(project_name, task_number, description):
    """Creates new task"""
    try:
        task = task_create(project_name, task_number, description)
        print_success("Task created successfully")
        print_tasks(task)
    except Exception:
        traceback.print_exc()
        print_fail("Failed to create task")

@tasks.command("find")
@click.argument("project_name")
@click.argument("task_number")
def cli_task_find(project_name, task_number):
    """Find task by project name and task number. Returns one task or None"""
    task = task_find(project_name, task_number)
    if task is None:
        print_success("Not found task with project name {0} and task number {1}".format(project_name, task_number))
    else:
        print_success("Found task with project name {0} and task number {1}".format(project_name, task_number))
        print_tasks(task)

@tasks.command("search")
@click.option("--project_name")
@click.option("--task_number")
@click.option("--is_closed", type=bool)
@click.option("--end_date")
@click.option("--date_operator", type=click.Choice(["eq", "lt", "gt", "le", "ge"]))
def cli_task_search(project_name, task_number, is_closed, end_date, date_operator):
    """Search tasks by criteria. Returns list of tasks"""
    tasks = task_search(project_name, is_closed, task_number, end_date, date_operator)
    print_success("Search properly finished")
    print_tasks(tasks)

@tasks.command("update")
@click.argument("project_name")
@click.argument("task_number")
@click.option("--description")
@click.option("--end_date")
@click.option("--user_external_id")
def cli_task_update(project_name, task_number, description, end_date, user_external_id):
    """Updates existing task"""
    try:
        user = user_find(user_external_id)
        task = task_update(project_name, task_number, description, end_date, user)
        print_success("Successfuly updated task number: {0} of project: {1}".format(task_number, project_name))
        print_tasks(task)
    except Exception as e:
        if isinstance(e, Task.DoesNotExist):
            print_fail("not found task to update, task number: {0} of project: {1}".format(task_number, project_name))
        else:
            traceback.print_exc()
            print_fail("Failed to update task, task number: {0} of project: {1}".format(task_number, project_name))

@tasks.command("delete")
@click.argument("project_name")
@click.argument("task_number")
def cli_task_delete(project_name, task_number):
    """Delete task with provided task number and project name. Returns total deleted tasks"""
    task_delete(project_name, task_number)
    print_success("Successfuly deleted task, task number: {0} of project: {1}".format(task_number, project_name))

def print_tasks(tasks):
    headers = ["Task number", "Project name", "Description", "end date", "User assigned (external_id)"]
    rows = []
    if tasks is None:
        tasks = []
    elif isinstance(tasks, Task):
        tasks = [tasks]
    for task in tasks:
        user_details = None
        if task.user != None:
            user_details = "{} ({})".format(task.user.user_name, task.user.external_id)
        rows.append([task.task_number, task.project.project_name, task.description, task.end_date, user_details])
    click.secho(tabulate(rows, headers=headers, tablefmt="psql"))
