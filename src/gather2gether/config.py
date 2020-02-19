import configparser
import os
import logging

logger = logging.getLogger("gather2gether-config")

def readConfig():
    # get path to config file from system env
    configPath = "."
    try:
        configPath = os.environ['G2G_CONF_PATH']
    except KeyError:
        logger.info("config path not provided")
    if len(configPath) > 1 and configPath.endswith("/"):
        configPath = configPath[:-1]
    logger.info("config path: {0}".format(configPath))
    # config from properties file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(configPath + "/gather2gether.properties")
    return config
