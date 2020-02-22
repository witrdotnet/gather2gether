import logging
from gather2gether.db import User

logger = logging.getLogger("g2g-dao-user")

def user_create(external_id, user_name):
    logger.info("about to save user external id:{0}, name:{1}".format(external_id, user_name))
    try:
        user = User.get(User.external_id == external_id)
        logger.info("already exists user id:{0}".format(external_id))
    except User.DoesNotExist:
        user = User(external_id = external_id, user_name = user_name)
        user.save()
        logger.info("saved new user id:{0}, name:{1}".format(external_id, user_name))

def user_update(external_id, user_name, is_active):
    logger.info("about to update user external id:{0}, name:{1}, active:{2}".format(external_id, user_name, is_active))
    try:
        user = User.get(User.external_id == external_id)
        if user_name != None:
            user.user_name = user_name
        if is_active != None:
            user.is_active = is_active
        user.save()
    except User.DoesNotExist:
        logger.error("not found user to update, external id:{0}".format(external_id))
