import unittest

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.user import *
from gather2gether.db.project import project_search, project_delete
from gather2gether.db.task import task_delete, task_search

import logging
logging.disable(None)

class TestUserDao(unittest.TestCase):

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

    def test_user_create_find(self):
        # WHEN
        user_create("A10", "Kathir")
        # THEN
        found_user = user_find("A10")
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.user_name, "Kathir")
        self.assertEqual(found_user.is_active, False)

    def test_user_update_find(self):
        # GIVEN
        user_create("A20", "Azzaaaaa")
        # WHEN
        user_update("A20", "Azza", True)
        # THEN
        found_user = user_find("A20")
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.user_name, "Azza")
        self.assertEqual(found_user.is_active, True)

    def test_user_search(self):
        # GIVEN
        user_create("A100", "Kais")
        user_update("A100", "Kais", True)
        user_create("A101", "Leila")
        user_update("A101", "Leila", True)
        user_create("A102", "Antar")
        user_create("A103", "Abla")

        # search all users
        found_users = user_search()
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 4)

        # search active users 
        found_users = user_search(is_active=True)
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 2)

        # search user with external id
        found_users = user_search(external_id="A100")
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 1)

        # search user with user_name
        found_users = user_search(user_name="Leila")
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 1)

        # search user with user_name and active
        found_users = user_search(user_name="Leila", is_active=True)
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 1)

        # search user with user_name and incorrect active value
        found_users = user_search(user_name="Leila", is_active=False)
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 0)

    def test_user_delete(self):
        # GIVEN
        user_create("B10", "Jamil")
        user_create("B11", "Bouthayna")
        found_users = user_search(user_name="Jamil")
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 1)
        # WHEN
        deleted_user_count = user_delete("B10")
        # THEN
        self.assertEqual(deleted_user_count, 1)
        found_users = user_search(user_name="Jamil")
        self.assertIsNotNone(found_users)
        self.assertEqual(len(found_users), 0)
