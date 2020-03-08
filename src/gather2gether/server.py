import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

class Server(object):
    def __init__(self, flask_app, version):
        self.logger = logging.getLogger('g2g-server')
        # TODO: get version from setup
        self.version = version
        self.flask_app = flask_app
        self.http_port = 8080
        self.host = '0.0.0.0'
        self.debug = False

    def __str__(self):
        return("gather2gether server")

    def start(self):
        self.logger.info(self.get_ascii_art())
        self.flask_app.run(host=self.host, port=self.http_port, debug=self.debug)

    def get_ascii_art(self):
        return """
              _   _                 ____               _   _               
   __ _  __ _| |_| |__   ___ _ __  |___ \    __ _  ___| |_| |__   ___ _ __ 
  / _` |/ _` | __| '_ \ / _ \ '__|   __) |  / _` |/ _ \ __| '_ \ / _ \ '__|
 | (_| | (_| | |_| | | |  __/ |     / __/  | (_| |  __/ |_| | | |  __/ |   
  \__, |\__,_|\__|_| |_|\___|_|    |_____|  \__, |\___|\__|_| |_|\___|_|   
  |___/                                     |___/                          
                                                         Version: {0}      
        """.format(self.version)

