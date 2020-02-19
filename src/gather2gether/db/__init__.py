import logging
from peewee import *
import datetime
import time

logger = logging.getLogger("g2g-db")

def create_database(db_name, db_host, db_port, db_user, db_password):
    return MySQLDatabase(
        db_name,
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password)

def init_database(db):
    # wait for database to be ready
    logger.info("check if database server is ready")
    wait_for_db_connection(db, 10, 3)
    logger.info("database server is up")
    with db:
        db.create_tables([User, Project, Task])

def wait_for_db_connection(db, max_tries, sleep_duration_in_seconds):
    try_count = 0
    while True:
        try_count += 1
        try:
            db.connect()
            logger.info("database server connection try {0}: OK".format(try_count))
            return
        except Exception as error:
            if try_count < max_tries:
                logger.info("database server connection try {0}: FAILED {1} {2}".format(try_count, db.connect_params, error))
                time.sleep(sleep_duration_in_seconds)
                pass
            else:
                logger.error("database server connection reached max tries. Unable to connect to DB")
                logger.exception(error)
                raise

from gather2gether.config import *
config = readConfig()
db_host = config.get('database', 'host')
db_port = config.getint('database', 'port')
db_name = config.get('database', 'db_name')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')
logger.info("init database mysql://{0}:{1}/{2}".format(db_host, db_port, db_name))

g2gDB = create_database(db_name, db_host, db_port, db_user, db_password)

class BaseModel(Model):
    class Meta:
        database = g2gDB

class User(BaseModel):
    external_id = CharField(unique=True)
    name = CharField(unique=False)
    created_date = DateTimeField(default=datetime.datetime.now)
    is_authorized = BooleanField(default=False)

class Project(BaseModel):
    name = CharField(unique=False)
    description = CharField(unique=False)
    created_date = DateTimeField(default=datetime.datetime.now)
    planned_start_date = DateTimeField()
    planned_end_date = DateTimeField()
    closed_date = DateTimeField()

class Task(BaseModel):
    user = ForeignKeyField(User, backref='tasks')
    project = ForeignKeyField(Project, backref='tasks')
    task_number = IntegerField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_finished = BooleanField(default=False)