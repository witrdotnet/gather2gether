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
    # check config file exists
    configFilePath = configPath + "/gather2gether.properties"
    if os.path.exists(configFilePath):
        # config from properties file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(configPath + "/gather2gether.properties")
        return config
    else:
        logger.error("not found config file {0}".format(configFilePath))
        raise EnvironmentError("not found config file " + configFilePath)

