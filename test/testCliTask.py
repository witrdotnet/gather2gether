import unittest
import click
from click.testing import CliRunner

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.project import project_create, project_search, project_delete
from gather2gether.db.task import task_delete, task_search, task_create, task_update, task_find
from gather2gether.db.user import user_create, user_search, user_delete

from gather2gether.cli_task import cli_task_create,cli_task_update, cli_task_find, cli_task_search, cli_task_delete

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

    def test_cli_task_create_with_project_name_not_exists(self):
        project_identifier = "test_cli_task_create_with_project_name_not_exists"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_create, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to create task", result.output)

    def test_cli_task_create_with_project_id_not_exists(self):
        project_identifier = "-50"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_create, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to create task", result.output)

    def test_cli_task_create_with_project_name_exists(self):
        project_identifier = "test_cli_task_create_with_project_name_exists"
        project_create(project_identifier)
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_create, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Task created successfully", result.output)

    def test_cli_task_create_with_project_id_exists(self):
        project = project_create("test_cli_task_create_with_project_id_exists")
        project_identifier = str(project.id)
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_create, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Task created successfully", result.output)

    def test_cli_task_find_with_project_name_not_exists(self):
        project_identifier = "test_cli_task_find_with_project_name_not_exists"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_find, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Not found task with project {0} and task number {1}".format(project_identifier, task_number), result.output)

    def test_cli_task_find_with_project_id_not_exists(self):
        project_identifier = "-50"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_find, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Not found task with project {0} and task number {1}".format(project_identifier, task_number), result.output)

    def test_cli_task_find_with_project_name_exists(self):
        project_identifier = "test_cli_task_find_with_project_name_exists"
        project_create(project_identifier)
        task_number = "1"
        task_create(project_identifier, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_find, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Found task with project {0} and task number {1}".format(project_identifier, task_number), result.output)

    def test_cli_task_find_with_project_id_exists(self):
        project = project_create("test_cli_task_find_with_project_id_exists")
        project_identifier = str(project.id)
        task_number = "1"
        task_create(project.id, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_find, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Found task with project {0} and task number {1}".format(project_identifier, task_number), result.output)

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
        task_create(project_identifier, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_update, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_update_by_project_id_exists(self):
        project = project_create("test_cli_task_update_by_project_id_exists")
        project_identifier = str(project.id)
        task_number = "1"
        task_create(project.project_name, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_update, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_update_set_user(self):
        user = user_create("A10", "Kathir")
        project_identifier = "test_cli_task_update_set_user"
        project_create(project_identifier)
        task_number = "1"
        task = task_create(project_identifier, task_number)
        self.assertIsNone(task.user)
        runner = CliRunner()
        result = runner.invoke(cli_task_update, [project_identifier, task_number, "--user_external_id", user.external_id])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier), result.output)
        task_after_update = task_find(project_identifier, task_number)
        self.assertEqual(task_after_update.user, user)

    def test_cli_task_update_reset_user(self):
        user = user_create("A10", "Kathir")
        project_identifier = "test_cli_task_update_reset_user"
        project_create(project_identifier)
        task_number = "1"
        task_create(project_identifier, task_number)
        task = task_update(project_identifier, task_number, user=user)
        self.assertIsNotNone(task.user)
        runner = CliRunner()
        result = runner.invoke(cli_task_update, [project_identifier, task_number, "--user_external_id", ""])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated task number: {0} of project: {1}".format(task_number, project_identifier), result.output)
        task_after_update = task_find(project_identifier, task_number)
        self.assertIsNone(task_after_update.user)

    def test_cli_task_delete_with_project_name_not_exists(self):
        project_identifier = "test_cli_task_delete_with_project_name_not_exists"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_delete, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to delete task, task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_delete_with_project_id_not_exists(self):
        project_identifier = "-50"
        task_number = "1"
        runner = CliRunner()
        result = runner.invoke(cli_task_delete, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to delete task, task number: {0} of project: {1}".format(task_number, project_identifier), result.output)

    def test_cli_task_delete_with_project_name_exists(self):
        project_identifier = "test_cli_task_delete_with_project_name_exists"
        project_create(project_identifier)
        task_number = "1"
        task_create(project_identifier, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_delete, [project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly deleted task, task number: {0} of project: {1}".format(task_number, project_identifier), result.output)
        task_after_delete = task_find(project_identifier, task_number)
        self.assertIsNone(task_after_delete)

    def test_cli_task_delete_with_project_id_exists(self):
        project = project_create("test_cli_task_delete_with_project_id_exists")
        project_identifier = str(project.id)
        task_number = "1"
        task_create(project.id, task_number)
        runner = CliRunner()
        result = runner.invoke(cli_task_delete, ["--identifier_type", "id", "--", project_identifier, task_number])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly deleted task, task number: {0} of project: {1}".format(task_number, project_identifier), result.output)
        task_after_delete = task_find(project_identifier, task_number)
        self.assertIsNone(task_after_delete)
