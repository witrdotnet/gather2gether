import unittest
import click
from click.testing import CliRunner

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.project import project_create, project_search, project_delete
from gather2gether.db.task import task_delete, task_search, task_create
from gather2gether.db.user import user_create, user_search, user_delete

from gather2gether.cli_task import cli_task_update

import logging
logging.disable(logging.NOTSET)

class TestCliTask(unittest.TestCase):

    def setUp(self):
        # delete all tasks in database
        found_tasks = task_search()
        for task in found_tasks:
            task_delete(task.project.project_name, task.task_number)
        # delete all projects in database
        found_projects = project_search()
        for project in found_projects:
            project_delete(project.project_name)
        # delete all users in database
        found_users = user_search()
        for user in found_users:
            user_delete(user.external_id)

    def test_cli_task_update_by_project_name_not_exists(self):
        project_identifier = "test_cli_task_update_by_project_name_not_exists"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_update, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to update task, task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_update_by_project_id_not_exists(self):
        project_identifier = "-50"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_update, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to update task, task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_update_by_project_name_exists(self):
        project_identifier = "test_cli_task_update_by_project_name_exists"
        project_create(project_identifier)
        task_number = "1"
        task = task_create(project_identifier, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_update, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_update_by_project_id_exists(self):
        project = project_create("test_cli_task_update_by_project_id_exists")
        project_identifier = str(project.id)
        task_number = "1"
        task = task_create(project.project_name, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_update, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier), result.output)
