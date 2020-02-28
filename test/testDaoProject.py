import unittest

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.project import *
from gather2gether.db.task import task_delete, task_search
from gather2gether.db.user import user_create, user_search, user_delete

import logging
logging.disable(None)

class TestProjectDao(unittest.TestCase):

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

    def test_project_create_find(self):
        # WHEN
        project_create("Project CREATE")
        # THEN
        found_project = project_find("Project CREATE")
        self.assertIsNotNone(found_project)
        self.assertEqual(found_project.project_name, "Project CREATE")
        self.assertIsNone(found_project.description)
        self.assertIsNone(found_project.planned_start_date)
        self.assertIsNone(found_project.planned_end_date)
        self.assertIsNone(found_project.closed_date)

    def test_project_create_full_find(self):
        # WHEN
        project_create("Project FULL", "proj FULL", "2020-01-01", "2020-01-5")
        # THEN
        found_project = project_find("Project FULL")
        self.assertIsNotNone(found_project)
        self.assertEqual(found_project.project_name, "Project FULL")
        self.assertEqual(found_project.description, "proj FULL")
        self.assertEqual(found_project.planned_start_date, datetime.datetime(2020, 1, 1, 0, 0))
        self.assertEqual(found_project.planned_end_date, datetime.datetime(2020, 1, 5, 0, 0))
        self.assertIsNone(found_project.closed_date)

    def test_project_update_find(self):
        # GIVEN
        project_create("Project UPDATE")
        # WHEN
        project_update("Project UPDATE", "Project UPDATE updated")
        # THEN
        found_project = project_find("Project UPDATE updated")
        self.assertEqual(found_project.project_name, "Project UPDATE updated")
        self.assertIsNone(found_project.description)
        self.assertIsNone(found_project.planned_start_date)
        self.assertIsNone(found_project.planned_end_date)
        self.assertIsNone(found_project.closed_date)

    def test_project_update_full_find(self):
        # GIVEN
        project_create("Project UPDATE FULL")
        # WHEN
        project_update("Project UPDATE FULL", "Project UPDATE FULL updated", "proj UPDATE FULL", "2020-01-10", "2020-01-15", "2020-01-13")
        # THEN
        found_project = project_find("Project UPDATE FULL updated")
        self.assertEqual(found_project.project_name, "Project UPDATE FULL updated")
        self.assertEqual(found_project.description, "proj UPDATE FULL")
        self.assertEqual(found_project.planned_start_date, datetime.datetime(2020, 1, 10, 0, 0))
        self.assertEqual(found_project.planned_end_date, datetime.datetime(2020, 1, 15, 0, 0))
        self.assertEqual(found_project.closed_date, datetime.datetime(2020, 1, 13, 0, 0))
