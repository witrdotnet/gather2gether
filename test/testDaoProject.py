import unittest

# init database
from gather2gether.db import g2gDB
from gather2gether.db import *
init_database(g2gDB)

from gather2gether.db.project import *
from gather2gether.db.task import task_delete, task_search
from gather2gether.db.user import user_create, user_search, user_delete

import logging
logging.disable(logging.INFO)

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

    def test_project_create_find_by_name(self):
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

    def test_project_create_find_by_id(self):
        # WHEN
        project = project_create("Project CREATE")
        # THEN
        found_project = project_find(project.id)
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

    def test_project_update_find_by_name(self):
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

    def test_project_update_find_by_id(self):
        # GIVEN
        project = project_create("test_project_update_find_by_id")
        # WHEN
        project_update(project.id, "Project UPDATE updated")
        # THEN
        found_project = project_find(project.id)
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

    def test_project_reset_closed_date(self):
        # GIVEN
        project_identifier = "test_task_reset_end_date"
        project_create(project_identifier)
        project_update(project_identifier, closed_date="2020-01-01")
        # WHEN
        project_update(project_identifier, closed_date="")
        # THEN
        found_project = project_find(project_identifier)
        self.assertIsNotNone(found_project)
        self.assertIsNone(found_project.closed_date)

    def test_project_search_existing(self):
        # GIVEN
        project_identifier = "test_task_reset_end_date"
        project_create(project_identifier)
        # WHEN
        found_projects = project_search(project_name=project_identifier)
        # THEN
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)

    def test_project_search_not_existing(self):
        # WHEN
        found_projects = project_search(project_name="test_project_search_not_existing")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 0)

    def test_project_search_by_closed_state(self):
        # GIVEN
        expected_project_name = "test_project_search_by_closed_state"
        project_create(expected_project_name)
        project = project_update(expected_project_name, closed_date="2020-01-31")
        # WHEN search is_closed=True (closed_date not NULL)
        found_projects = project_search(project_name=expected_project_name, is_closed=True)
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search is_closed=False (closed_date is NULL)
        found_projects = project_search(project_name=expected_project_name, is_closed=False)
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 0)

    def test_project_search_by_planned_start_date(self):
        # GIVEN
        expected_project_name = "test_project_search_by_planned_start_date"
        expected_start_date = "2020-01-31"
        project_create(expected_project_name)
        project = project_update(expected_project_name, planned_start_date=expected_start_date)
        # WHEN search eq start_date
        found_projects = project_search(project_name=expected_project_name, date_filter="start", date=expected_start_date, date_operator="eq")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search lt start_date
        found_projects = project_search(project_name=expected_project_name, date_filter="start", date="2020-02-01", date_operator="lt")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search gt closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="start", date="2020-01-01", date_operator="gt")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search le closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="start", date="2020-02-01", date_operator="le")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search ge closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="start", date="2020-01-01", date_operator="ge")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)

    def test_project_search_by_planned_end_date(self):
        # GIVEN
        expected_project_name = "test_project_search_by_planned_end_date"
        expected_end_date = "2020-01-31"
        project_create(expected_project_name)
        project = project_update(expected_project_name, planned_end_date=expected_end_date)
        # WHEN search eq end_date
        found_projects = project_search(project_name=expected_project_name, date_filter="end", date=expected_end_date, date_operator="eq")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search lt end_date
        found_projects = project_search(project_name=expected_project_name, date_filter="end", date="2020-02-01", date_operator="lt")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search gt closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="end", date="2020-01-01", date_operator="gt")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search le closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="end", date="2020-02-01", date_operator="le")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search ge closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="end", date="2020-01-01", date_operator="ge")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)

    def test_project_search_by_closed_date(self):
        # GIVEN
        expected_project_name = "test_project_search_by_closed_date"
        expected_closed_date = "2020-01-31"
        project_create(expected_project_name)
        project = project_update(expected_project_name, closed_date=expected_closed_date)
        # WHEN search eq closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="closed", date=expected_closed_date, date_operator="eq")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search lt closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="closed", date="2020-02-01", date_operator="lt")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search gt closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="closed", date="2020-01-01", date_operator="gt")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search le closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="closed", date="2020-02-01", date_operator="le")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)
        # WHEN search ge closed_date
        found_projects = project_search(project_name=expected_project_name, date_filter="closed", date="2020-01-01", date_operator="ge")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)

    def test_project_search_by_all_criteria(self):
        # GIVEN
        expected_project_name = "test_project_search_by_all_criteria"
        expected_project_description = "desc test_project_search_by_all_criteria"
        expected_end_date = "2020-01-31"
        project_create(expected_project_name)
        project = project_update(expected_project_name, description=expected_project_description, planned_end_date=expected_end_date)
        # WHEN
        found_projects = project_search(project_name=expected_project_name, is_closed=False, date_filter="end", date=expected_end_date, date_operator="eq")
        self.assertIsNotNone(found_projects)
        self.assertEqual(len(found_projects), 1)
        self.assertEqual(found_projects[0], project)

    def test_project_delete_existing_by_name(self):
        # GIVEN
        project_identifier = "test_project_delete_existing_by_name"
        project_create(project_identifier)
        # WHEN
        total_deleted = project_delete(project_identifier)
        # THEN
        self.assertEqual(total_deleted, 1)
        found_project = project_find(project_identifier)
        self.assertIsNone(found_project)

    def test_project_delete_existing_by_id(self):
        # GIVEN
        project = project_create("test_project_delete_existing_by_id")
        project_identifier = project.id
        # WHEN
        total_deleted = project_delete(project_identifier)
        # THEN
        self.assertEqual(total_deleted, 1)
        found_project = project_find(project_identifier)
        self.assertIsNone(found_project)

    def test_project_delete_not_existing_by_name(self):
        # GIVEN
        project_identifier = "test_project_delete_not_existing_by_name"
        # WHEN
        total_deleted = project_delete(project_identifier)
        # THEN
        self.assertEqual(total_deleted, 0)

    def test_project_delete_not_existing_by_id(self):
        # GIVEN
        project_identifier = -50
        # WHEN
        total_deleted = project_delete(project_identifier)
        # THEN
        self.assertEqual(total_deleted, 0)
