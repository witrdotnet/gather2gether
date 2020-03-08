import configparser
import os
import logging

logger = logging.getLogger("gather2gether-config")

def read_config():
    # get path to config file from system env
    config_path = "."
    try:
        config_path = os.environ['G2G_CONF_PATH']
    except KeyError:
        logger.info("config path not provided")
    if len(config_path) > 1 and config_path.endswith("/"):
        config_path = config_path[:-1]
    logger.info("config path: {0}".format(config_path))
    # check config file exists
    config_file_path = config_path + "/gather2gether.properties"
    if os.path.exists(config_file_path):
        # config from properties file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(config_path + "/gather2gether.properties")
        return config
    else:
        logger.error("not found config file {0}".format(config_file_path))
        raise EnvironmentError("not found config file " + config_file_path)

