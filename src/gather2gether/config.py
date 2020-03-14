import configparser
import os
import logging

logger = logging.getLogger("gather2gether-config")

def read_config():
    default_config_file = "./gather2gether.properties"
    # get path to config file from system env
    config_file = default_config_file
    try:
        config_file = os.environ['G2G_CONF_FILE']
    except KeyError:
        logger.info("Config path not provided")
    if len(config_file.strip()) == 0:
        config_file = default_config_file
    logger.info("Config path: {0}".format(config_file))
    # check config file exists
    if os.path.exists(config_file):
        # config from properties file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(config_file)
        return config
    else:
        logger.error("Not found config file {0}".format(config_file))
        raise EnvironmentError("not found config file " + config_file)

