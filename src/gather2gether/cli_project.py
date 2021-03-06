from gather2gether.db.project import *
from gather2gether.cli import print_success, print_fail

import click
from flask.cli import AppGroup
from tabulate import tabulate
import traceback

import logging
logging.disable(logging.INFO)

projects = AppGroup("projects")

@projects.command("create")
@click.argument("project_name")
@click.option("--description")
@click.option("--planned_start_date")
@click.option("--planned_end_date")
def cli_project_create(project_name, description, planned_start_date, planned_end_date):
    """Creates new project"""
    try:
        project = project_create(project_name, description, planned_start_date, planned_end_date)
        print_success("Project created successfully")
        print_projects(project)
    except Exception:
        traceback.print_exc()
        print_fail("Failed to create project")

@projects.command("find")
@click.argument("project_identifier")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
def cli_project_find(project_identifier, identifier_type):
    """Find project by its identifier. Returns one project or None"""
    project_identifier_arg = project_identifier
    logger.info("find project by {0} = {1}".format(identifier_type, project_identifier))
    if identifier_type == "id":
        project_identifier_arg = int(project_identifier)
    project = project_find(project_identifier_arg)
    if project is None:
        print_success("Not found project with identifier {0}".format(project_identifier))
    else:
        print_success("Found project with identifier {0}".format(project_identifier))
        print_projects(project)

@projects.command("search")
@click.option("--project_name")
@click.option("--is_closed", type=bool)
@click.option("--date")
@click.option("--date_filter", type=click.Choice(["start", "end", "close"]))
@click.option("--date_operator", type=click.Choice(["eq", "lt", "gt", "le", "ge"]))
def cli_project_search(project_name, is_closed, date, date_filter, date_operator):
    """Search projects by criteria. Returns list of projects"""
    projects = project_search(project_name, is_closed, date, date_filter, date_operator)
    print_success("Search properly finished")
    print_projects(projects)

@projects.command("update")
@click.argument("project_identifier")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
@click.option("--project_name")
@click.option("--description")
@click.option("--planned_start_date")
@click.option("--planned_end_date")
@click.option("--closed_date")
def cli_project_update(project_identifier, identifier_type, project_name, description, planned_start_date, planned_end_date, closed_date):
    """Updates existing project"""
    project_identifier_arg = project_identifier
    logger.info("about to update project by {0} = {1}".format(identifier_type, project_identifier))
    if identifier_type == "id":
        project_identifier_arg = int(project_identifier)
    try:
        project = project_update(project_identifier_arg, project_name, description, planned_start_date, planned_end_date, closed_date)
        print_success("Successfuly updated project name: {0}".format(project_identifier))
        print_projects(project)
    except Exception as e:
        if isinstance(e, Project.DoesNotExist):
            print_fail("Not found project to update, name:{0}".format(project_identifier))
        else:
            traceback.print_exc()
            print_fail("Failed to update project with name: {0}".format(project_identifier))

@projects.command("delete")
@click.argument("project_identifier")
@click.option("--identifier_type", type=click.Choice(["name", "id"]), default="name")
def cli_project_delete(project_identifier, identifier_type):
    """Delete project with provided name. Returns total deleted projects"""
    project_identifier_arg = project_identifier
    logger.info("about to delete project by {0} = {1}".format(identifier_type, project_identifier))
    if identifier_type == "id":
        project_identifier_arg = int(project_identifier)
    project_delete(project_identifier_arg)
    print_success("Successfuly deleted project name: {0}".format(project_identifier))

def print_projects(projects):
    headers = ["Id", "Name", "Description", "Planned start date", "Planned end date", "Close date"]
    rows = []
    if projects is None:
        projects = []
    elif isinstance(projects, Project):
        projects = [projects]
    for project in projects:
        rows.append([project.id, project.project_name, project.description, project.planned_start_date, project.planned_end_date, project.closed_date])
    click.secho(tabulate(rows, headers=headers, tablefmt="psql"))
