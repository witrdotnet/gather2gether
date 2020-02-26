import logging
from gather2gether.db import User

logger = logging.getLogger("g2g-dao-user")

def user_create(external_id, user_name):
    logger.info("about to create user external id:{0}, name:{1}".format(external_id, user_name))
    try:
        user = User.get(User.external_id == external_id)
        logger.info("already exists user external id:{0}".format(external_id))
        raise Exception("already exists user external id:{0}".format(external_id))
    except User.DoesNotExist:
        user = User(external_id = external_id, user_name = user_name)
        user.save()
        logger.info("saved new user external id:{0}, name:{1}".format(external_id, user_name))
        return user

def user_find(external_id):
    logger.info("about to find user by external id:{0}".format(external_id))
    try:
        user = User.get(User.external_id == external_id)
        return user
    except User.DoesNotExist:
        return None

def user_search(external_id=None, user_name=None, is_active=None):
    logger.info("about to search user by criteria, external id:{0}, name:{1}, active:{2}".format(external_id, user_name, is_active))
    clauses = True
    if not external_id is None:
        clauses &= (User.external_id == external_id)
    if not user_name is None:
        clauses &= (User.user_name == user_name)
    if not is_active is None:
        clauses &= (User.is_active == is_active)
    users = User.select().where(clauses)
    logger.info("found users by criteria, external id:{0}, name:{1}, active:{2}".format(external_id, user_name, is_active))
    for user in users:
        logger.debug("\t\t- {0}\t{1}".format(user.external_id, user.user_name))
    return users

def user_update(external_id, user_name, is_active):
    logger.info("about to update user external id:{0}, name:{1}, active:{2}".format(external_id, user_name, is_active))
    try:
        user = User.get(User.external_id == external_id)
        if user_name != None:
            user.user_name = user_name
        if is_active != None:
            user.is_active = is_active
        user.save()
        return user
    except User.DoesNotExist:
        logger.error("not found user to update, external id:{0}".format(external_id))
        raise

def user_delete(external_id):
    logger.info("about to delete user by external id:{0}".format(external_id))
    query = User.delete().where(User.external_id == external_id)
    total_deleted = query.execute()
    logger.info("{0} deleted user".format(total_deleted))
    return total_deleted
