from gather2gether.server import Server
from flask import Flask

import os

currentPath = os.path.dirname(os.path.realpath(__file__))
versionFilePathName = os.path.join(currentPath,'VERSION')

__version__ = 'unknown'
with open(versionFilePathName, "r") as version_file:
    __version__ = version_file.read().strip()

app = Flask(__name__)
g2gServer = Server(app, __version__)

from gather2gether import routes
from gather2gether import cli
