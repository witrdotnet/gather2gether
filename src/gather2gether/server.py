import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

class Server(object):
    def __init__(self, flaskApp, version):
        self.logger = logging.getLogger('g2g-server')
        # TODO: get version from setup
        self.version = version
        self.flaskApp = flaskApp
        self.httpPort = 8080
        self.host = '0.0.0.0'
        self.debug = False

    def __str__(self):
        return("gather2gether server")

    def start(self):
        self.logger.info(self.getAsciiArt())
        self.flaskApp.run(host=self.host, port=self.httpPort, debug=self.debug)

    def getAsciiArt(self):
        return """
              _   _                 ____               _   _               
   __ _  __ _| |_| |__   ___ _ __  |___ \    __ _  ___| |_| |__   ___ _ __ 
  / _` |/ _` | __| '_ \ / _ \ '__|   __) |  / _` |/ _ \ __| '_ \ / _ \ '__|
 | (_| | (_| | |_| | | |  __/ |     / __/  | (_| |  __/ |_| | | |  __/ |   
  \__, |\__,_|\__|_| |_|\___|_|    |_____|  \__, |\___|\__|_| |_|\___|_|   
  |___/                                     |___/                          
                                                         Version: {0}      
        """.format(self.version)

