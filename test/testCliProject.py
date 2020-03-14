import unittest
import click
from click.testing import CliRunner

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.project import project_create, project_search, project_delete
from gather2gether.db.task import task_delete, task_search
from gather2gether.db.user import user_create, user_search, user_delete

from gather2gether.cli_project import cli_project_find

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
        project_identifier = "test_cli_project_find_exists"
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
