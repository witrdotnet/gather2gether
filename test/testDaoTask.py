import unittest

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.task import *
from gather2gether.db.project import project_create, project_search, project_delete
from gather2gether.db.user import user_create, user_search, user_delete

import logging
logging.disable(None)

class TestTaskDao(unittest.TestCase):

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

    def test_task_create_find(self):
        # GIVEN
        project_create("PROJ4Task1")
        # WHEN
        task_create("PROJ4Task1", 1)
        # THEN
        found_task = task_find("PROJ4Task1",1)
        self.assertIsNotNone(found_task)

    def test_task_update_find(self):
        # GIVEN
        project_create("PROJ4Task2")
        task_create("PROJ4Task2", 2)
        user = user_create("USER4TASK2", "Mr. Lazy")
        # WHEN
        task_update("PROJ4Task2", 2, "description task 2", "2020-01-01", user)
        # THEN
        found_task = task_find("PROJ4Task2",2)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.description, "description task 2")
        self.assertEqual(found_task.end_date, datetime.datetime(2020, 1, 1, 0, 0))
        self.assertEqual(found_task.user, user)

    def test_task_search_by_user(self):
        # GIVEN
        project_create("PROJ4TaskSearch")
        task_create("PROJ4TaskSearch", 1)
        user = user_create("PROJ4TaskSearch", "Mr. Lazy")
        task_update("PROJ4TaskSearch", 1, user=user)
        # WHEN
        found_tasks = task_search(user_external_id=user.external_id)
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)

    def test_task_delete(self):
        # GIVEN
        project_create("PROJ4TaskDelete")
        task_create("PROJ4TaskDelete", 1)
        found_tasks = task_search(project_name="PROJ4TaskDelete", task_number=1)
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        # WHEN
        deleted_task_count = task_delete("PROJ4TaskDelete", 1)
        # THEN
        self.assertEqual(deleted_task_count, 1)
        found_tasks = task_search(project_name="PROJ4TaskDelete", task_number=1)
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 0)
