import unittest
from mock import Mock

from gather2gether.server import Server
from flask import Flask

import logging
logging.disable(None)

app = Flask("test")
app.run = Mock()
g2gServerTest = Server(app, "test")

class TestServer(unittest.TestCase):

    def test_server_to_str(self):
        # WHEN - THEN
        self.assertEqual(g2gServerTest.__str__(), "gather2gether server")

    def test_server_get_ascii_art(self):
        # WHEN - THEN
        self.assertIsNotNone(g2gServerTest.get_ascii_art())

    def test_server_start(self):
        # WHEN - THEN
        g2gServerTest.start()
        g2gServerTest.flask_app.run.assert_called_once()
