from gather2gether import app
from gather2gether import g2gServer
from gather2gether.db import g2gDB
from gather2gether.db import init_database

def main():
    init_database(g2gDB)
    g2gServer.start()    
