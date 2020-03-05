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

    def test_task_create_on_not_existing_project(self):
        # WHEN - THEN
        expected_project_name = "test_task_create_on_not_existing_project"
        with self.assertRaises(Exception) as context:
            task_create(expected_project_name, 1)
        self.assertIn("project {0} not Found".format(expected_project_name), context.exception.message)

    def test_task_create_already_existing(self):
        # GIVEN
        expected_project_name = "test_task_create_already_existing"
        project_create(expected_project_name)
        task_create(expected_project_name, 1)
        # WHEN - THEN
        with self.assertRaises(Exception) as context:
            task_create(expected_project_name, 1)
        self.assertIn("already exists task number", context.exception.message)

    def test_task_create_find(self):
        # GIVEN
        project_create("PROJ4Task1")
        # WHEN
        task_create("PROJ4Task1", 1)
        # THEN
        found_task = task_find("PROJ4Task1",1)
        self.assertIsNotNone(found_task)

    def test_task_find_not_existing_task_of_existing_project(self):
        # GIVEN
        project_create("RPOJ4test_task_find_not_existing")
        # THEN
        found_task = task_find("RPOJ4test_task_find_not_existing",1)
        self.assertIsNone(found_task)

    def test_task_find_not_existing_task_of_not_existing_project(self):
        # WHEN-THEN
        found_task = task_find("test_task_find_not_existing_task_of_not_existing_project",1)
        self.assertIsNone(found_task)

    def test_task_update_not_existing_task(self):
        # WHEN - THEN
        with self.assertRaises(Exception) as context:
            task_update("test_task_update_not_existing_task", 1, description="description task 2")
        self.assertIn("not found task to update", context.exception.message)

    def test_task_update_all_fields(self):
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

    def test_task_reset_end_date(self):
        # GIVEN
        expected_project_name = "test_task_reset_end_date"
        project_create(expected_project_name)
        task_create(expected_project_name, 1)
        task_update(expected_project_name, 1, end_date="2020-01-01")
        # WHEN
        task_update(expected_project_name, 1, end_date="")
        # THEN
        found_task = task_find(expected_project_name, 1)
        self.assertIsNotNone(found_task)
        self.assertIsNone(found_task.end_date)

    def test_task_reset_user(self):
        # GIVEN
        expected_project_name = "test_task_reset_user"
        project_create(expected_project_name)
        task_create(expected_project_name, 1)
        user = user_create("USERtest_task_reset_user", "Mr. Lazy")
        task_update(expected_project_name, 1, user=user)
        # WHEN
        task_update(expected_project_name, 1, user="")
        # THEN
        found_task = task_find(expected_project_name, 1)
        self.assertIsNotNone(found_task)
        self.assertIsNone(found_task.user)

    def test_task_search_not_existing_project(self):
        # WHEN
        found_tasks = task_search(project_name="test_task_search_not_existing")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 0)

    def test_task_search_not_existing_task(self):
        # GIVEN
        expected_project_name = "test_task_search_not_existing_task"
        project_create(expected_project_name)
        # WHEN
        found_tasks = task_search(project_name=expected_project_name, task_number=1)
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 0)

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

    def test_task_search_by_end_date(self):
        # GIVEN
        expected_project_name = "test_task_search_by_all_criteria"
        expected_end_date = "2020-01-31"
        project_create(expected_project_name)
        created_task = task_create(expected_project_name, 1)
        task_update(expected_project_name, 1, end_date=expected_end_date)
        # WHEN search is_closed=True (end_date not NULL)
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            is_closed=True)
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)
        # WHEN search is_closed=False (end_date is NULL)
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            is_closed=False)
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 0)
        # WHEN search eq end_date
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            end_date=expected_end_date, 
            date_operator="eq")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)
        # WHEN search lt end_date
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            end_date="2020-02-01", 
            date_operator="lt")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)
        # WHEN search gt end_date
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            end_date="2020-01-01", 
            date_operator="gt")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)
        # WHEN search le end_date
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            end_date="2020-02-01", 
            date_operator="le")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)
        # WHEN search ge end_date
        found_tasks = task_search(project_name=expected_project_name, 
            task_number=1, 
            end_date="2020-01-01", 
            date_operator="ge")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)

    def test_task_search_by_all_criteria(self):
        # GIVEN
        expected_project_name = "test_task_search_by_all_criteria"
        expected_task_description = "desc test_task_search_by_all_criteria"
        expected_end_date = "2020-01-31"
        project_create(expected_project_name)
        created_task = task_create(expected_project_name, 1)
        user = user_create(expected_project_name, "Mr. Lazy")
        task_update(expected_project_name, 1, 
            user=user, 
            description=expected_task_description,
            end_date=expected_end_date)
        # WHEN
        found_tasks = task_search(user_external_id=user.external_id, project_name=expected_project_name, is_closed=True, task_number=1, end_date=expected_end_date, date_operator="eq")
        self.assertIsNotNone(found_tasks)
        self.assertEqual(len(found_tasks), 1)
        self.assertEqual(found_tasks[0], created_task)

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

    def test_task_delete_not_existing_task(self):
        # GIVEN
        expected_project_name = "test_task_delete_not_existing_task"
        project_create(expected_project_name)
        # WHEN
        deleted_task_count = task_delete(expected_project_name, 1)
        # THEN
        self.assertEqual(deleted_task_count, 0)

    def test_task_delete_not_existing_project(self):
        # GIVEN
        expected_project_name = "test_task_delete_not_existing_project"
        # WHEN - THEN
        with self.assertRaises(Exception) as context:
            task_delete(expected_project_name, 1)
        self.assertIn("project {0} not Found".format(expected_project_name), context.exception.message)
