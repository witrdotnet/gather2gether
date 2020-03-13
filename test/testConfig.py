import unittest
import os
from gather2gether.config import read_config

import logging
logging.disable(logging.INFO)

class TestConfig(unittest.TestCase):

    def test_read_config_from_default_file(self):
        # GIVEN
        os.environ["G2G_CONF_PATH"] = ""
        # WHEN
        config = read_config()
        # THEN
        self.assertIsNotNone(config)
        self.assertEqual(config.get('database', 'host'), "127.0.0.1")
        self.assertEqual(config.getint('database', 'port'), 3307)
        self.assertEqual(config.get('database', 'db_name'), "gather2gether")
        self.assertEqual(config.get('database', 'user'), "g2g")
        self.assertEqual(config.get('database', 'password'), "g2g")

    def test_read_config_from_customized_file_path(self):
        # GIVEN
        os.environ["G2G_CONF_PATH"] = "./test"
        # WHEN
        config = read_config()
        # THEN
        self.assertIsNotNone(config)
        self.assertEqual(config.get('database', 'host'), "testDbHostName")
        self.assertEqual(config.getint('database', 'port'), 1234)
        self.assertEqual(config.get('database', 'db_name'), "testDbName")
        self.assertEqual(config.get('database', 'user'), "testDbUser")
        self.assertEqual(config.get('database', 'password'), "testDbPass")

    def test_read_config_from_customized_file_path_with_leading_slash(self):
        # GIVEN
        os.environ["G2G_CONF_PATH"] = "./test/"
        # WHEN
        config = read_config()
        # THEN
        self.assertIsNotNone(config)
        self.assertEqual(config.get('database', 'host'), "testDbHostName")
        self.assertEqual(config.getint('database', 'port'), 1234)
        self.assertEqual(config.get('database', 'db_name'), "testDbName")
        self.assertEqual(config.get('database', 'user'), "testDbUser")
        self.assertEqual(config.get('database', 'password'), "testDbPass")

    def test_read_config_from_not_found_file(self):
        # GIVEN
        expected_config_file_path = "./test_read_config_file_not_found"
        os.environ["G2G_CONF_PATH"] = expected_config_file_path
        # WHEN - THEN
        with self.assertRaises(EnvironmentError) as context:
            read_config()
        self.assertIn("not found config file " + expected_config_file_path, str(context.exception))
