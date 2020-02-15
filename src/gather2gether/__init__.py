from gather2gether.server import Server
from flask import Flask

app = Flask(__name__)
g2gServer = Server(app)

from gather2gether import routes