import unittest
import click
from click.testing import CliRunner

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.project import project_create, project_find, project_update, project_search, project_delete
from gather2gether.db.task import task_delete, task_search
from gather2gether.db.user import user_create, user_search, user_delete

from gather2gether.cli_project import cli_project_create, cli_project_find, cli_project_search, cli_project_update, cli_project_delete

import logging
logging.disable(logging.NOTSET)

class TestCliProject(unittest.TestCase):

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

    def test_cli_project_create(self):
        project_identifier = "test_cli_project_create"
        runner = CliRunner()
        result = runner.invoke(cli_project_create, [project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Project created successfully", result.output)
        project_found = project_find(project_identifier)
        self.assertIsNotNone(project_found)
        self.assertEqual(project_found.project_name, project_identifier)

    def test_cli_project_create_full(self):
        project_identifier = "test_cli_project_create"
        expected_description = "description of test_cli_project_create"
        expected_start_date = "2020-01-01"
        expected_end_date = "2020-01-10"
        runner = CliRunner()
        result = runner.invoke(cli_project_create, [
            project_identifier,
            "--description", expected_description,
            "--planned_start_date", expected_start_date,
            "--planned_end_date", expected_end_date
            ])
        self.assertIsNone(result.exception)
        self.assertIn("Project created successfully", result.output)
        project_found = project_find(project_identifier)
        self.assertIsNotNone(project_found)
        self.assertEqual(project_found.project_name, project_identifier)
        self.assertEqual(project_found.description, expected_description)
        self.assertEqual(project_found.planned_start_date, datetime.datetime.strptime(expected_start_date, "%Y-%m-%d"))
        self.assertEqual(project_found.planned_end_date, datetime.datetime.strptime(expected_end_date, "%Y-%m-%d"))

    def test_cli_project_create_already_exists(self):
        project_identifier = "test_cli_project_create_already_exists"
        project_create(project_identifier)
        runner = CliRunner()
        result = runner.invoke(cli_project_create, [project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Failed to create project", result.output)

    def test_cli_project_find_by_name_not_exists(self):
        project_identifier = "test_cli_project_find_by_name_not_exists"
        runner = CliRunner()
        result = runner.invoke(cli_project_find, [project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Not found project with identifier {0}".format(project_identifier), result.output)

    def test_cli_project_find_by_id_not_exists(self):
        project_identifier = "-50"
        runner = CliRunner()
        result = runner.invoke(cli_project_find, ["--identifier_type", "id", "--", project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Not found project with identifier {0}".format(project_identifier), result.output)

    def test_cli_project_find_by_name_exists(self):
        project_identifier = "test_cli_project_find_by_name_exists"
        project_create(project_identifier)
        runner = CliRunner()
        result = runner.invoke(cli_project_find, [project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Found project with identifier {0}".format(project_identifier), result.output)

    def test_cli_project_find_by_id_exists(self):
        project = project_create("test_cli_project_find_by_id_exists")
        project_identifier = str(project.id)
        runner = CliRunner()
        result = runner.invoke(cli_project_find, [project_identifier, "--identifier_type", "id"])
        self.assertIsNone(result.exception)
        self.assertIn("Found project with identifier {0}".format(project_identifier), result.output)

    def test_cli_project_search_closed(self):
        project_identifier = "test_cli_project_search_closed"
        project_create(project_identifier)
        project_update(project_identifier, closed_date="2020-01-01")
        runner = CliRunner()
        result = runner.invoke(cli_project_search, ["--is_closed", "true"])
        self.assertIsNone(result.exception)
        self.assertIn("Search properly finished", result.output)
        self.assertIn(project_identifier, result.output)
        result = runner.invoke(cli_project_search, ["--is_closed", "false"])
        self.assertIsNone(result.exception)
        self.assertIn("Search properly finished", result.output)
        self.assertNotIn(project_identifier, result.output)

    def test_cli_project_search_not_closed(self):
        project_identifier = "test_cli_project_search_not_closed"
        project_create(project_identifier)
        runner = CliRunner()
        result = runner.invoke(cli_project_search, ["--is_closed", "true"])
        self.assertIsNone(result.exception)
        self.assertIn("Search properly finished", result.output)
        self.assertNotIn(project_identifier, result.output)
        result = runner.invoke(cli_project_search, ["--is_closed", "false"])
        self.assertIsNone(result.exception)
        self.assertIn("Search properly finished", result.output)
        self.assertIn(project_identifier, result.output)

    def test_cli_project_update_by_name_exists(self):
        project_identifier = "test_cli_project_update_by_name_exists"
        expected_new_name = "test_cli_project_update_by_name_exists updated"
        project_create(project_identifier)
        runner = CliRunner()
        result = runner.invoke(cli_project_update, [project_identifier, "--project_name", expected_new_name])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated project name: {0}".format(project_identifier), result.output)
        project_found = project_find(project_identifier)
        self.assertIsNone(project_found)
        project_found = project_find(expected_new_name)
        self.assertIsNotNone(project_found)

    def test_cli_project_update_by_id_exists(self):
        expected_new_name = "test_cli_project_update_by_id_exists updated"
        project = project_create("test_cli_project_update_by_id_exists")
        project_identifier = str(project.id)
        runner = CliRunner()
        result = runner.invoke(cli_project_update, [project_identifier, "--identifier_type", "id", "--project_name", expected_new_name])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly updated project name: {0}".format(project_identifier), result.output)
        project_found = project_find(project.id)
        self.assertIsNotNone(project_found)
        self.assertEqual(project_found.project_name, expected_new_name)

    def test_cli_project_update_by_name_not_exists(self):
        project_identifier = "test_cli_project_update_by_name_exists"
        runner = CliRunner()
        result = runner.invoke(cli_project_update, [project_identifier, "--project_name", "new project name"])
        self.assertIsNone(result.exception)
        self.assertIn("Not found project to update, name:{0}".format(project_identifier), result.output)

    def test_cli_project_update_by_id_not_exists(self):
        project_identifier = "-50"
        runner = CliRunner()
        result = runner.invoke(cli_project_update, ["--identifier_type", "id", "--project_name", "new project name", "--", project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Not found project to update, name:{0}".format(project_identifier), result.output)

    def test_cli_project_delete_by_name(self):
        project_identifier = "test_cli_project_delete_by_name"
        project_create(project_identifier)
        runner = CliRunner()
        result = runner.invoke(cli_project_delete, [project_identifier])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly deleted project name: {0}".format(project_identifier), result.output)
        project_found = project_find(project_identifier)
        self.assertIsNone(project_found)

    def test_cli_project_delete_by_id(self):
        project = project_create("test_cli_project_delete_by_id")
        project_identifier = str(project.id)
        runner = CliRunner()
        result = runner.invoke(cli_project_delete, [project_identifier, "--identifier_type", "id"])
        self.assertIsNone(result.exception)
        self.assertIn("Successfuly deleted project name: {0}".format(project_identifier), result.output)
        project_found = project_find(project.id)
        self.assertIsNone(project_found)
