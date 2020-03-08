import unittest

from gather2gether import app

import logging
logging.disable(None)

class TestRoutes(unittest.TestCase):
    
    def test_server_root_route(self):
        with app.test_client() as routes:
            # WHEN
            response = routes.get("/")
            # THEN
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.data)
            self.assertIn("</pre>", response.data)
