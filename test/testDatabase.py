import unittest
from mock import Mock
from gather2gether.db import create_database, init_database, wait_for_db_connection

import logging
logging.disable(logging.INFO)

class TestDatabase(unittest.TestCase):

    def test_init_database(self):
        # GIVEN
        database = create_database("gather2gether", "127.0.0.1", 3307, "g2g", "g2g")
        database.create_tables = Mock()
        # WHEN
        init_database(database)
        # THEN
        database.create_tables.assert_called_once()

    def test_fail_database_connect(self):
        # GIVEN
        database = create_database("notexistingDB", "127.0.0.1", 3307, "badUser", "badPass")
        # WHEN - THEN
        with self.assertRaises(Exception) as context:
            wait_for_db_connection(database, 1, 1)
        self.assertIsNotNone(str(context.exception))