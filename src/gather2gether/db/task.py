import logging
from gather2gether.db import Task
from gather2gether.db import Project
from gather2gether.db.project import project_find

logger = logging.getLogger("g2g-dao-task")

def task_create(project_name, task_number, description = None):
    logger.info("about to create task in project:{0}, task number:{1}, description:{2}".format(project_name, task_number, description))
    project = project_find(project_name)
    if project is None:
        raise Exception("project {0} not Found".format(project_name))
    try:
        task = Task.get(Task.project == project, Task.task_number == task_number)
        logger.info("already exists task number:{0} in project:{1}".format(task_number, project_name))
        raise Exception("already exists task number:{0} in project:{1}".format(task_number, project_name))
    except Task.DoesNotExist:
        task = Task(project = project, task_number = task_number, description = description)
        task.save()
        logger.info("saved new task:{0} in project:{1}".format(task_number, project_name))
        return task

def task_find(project_name, task_number):
    logger.info("about to find task number:{0} in project:{1}".format(task_number, project_name))
    project = project_find(project_name)
    if project is None:
        return None
    try:
        task = Task.get(Task.project == project, Task.task_number == task_number)
        return task
    except Task.DoesNotExist:
        return None

def task_search(project_name=None, is_closed=None, task_number=None, end_date=None, date_operator=None):
    logger.info("about to search task by criteria, project_name:{0}, is_closed:{1}, end_date:{2}, date_operator:{3}".format(project_name, is_closed, end_date, date_operator))
    clauses = True
    if not project_name is None:
        project = project_find(project_name)
        if project is None:
            return []
        else:
            clauses &= (Task.project == project)
    if not is_closed is None:
        if is_closed:
            clauses &= (Task.end_date.is_null(False))
        else:
            clauses &= (Task.end_date.is_null())
    if not end_date is None and not date_operator is None:
        if date_operator == "eq":
            clauses &= (Task.end_date == end_date)
        elif date_operator == "gt":
            clauses &= (Task.end_date > end_date)
        elif date_operator == "lt":
            clauses &= (Task.end_date < end_date)
        elif date_operator == "ge":
            clauses &= (Task.end_date >= end_date)
        elif date_operator == "le":
            clauses &= (Task.end_date <= end_date)
    tasks = Task.select().where(clauses)
    logger.info("found tasks by criteria, project_name:{0}, is_closed:{1}, end_date:{2}, date_operator:{3}".format(project_name, is_closed, end_date, date_operator))
    for task in tasks:
        logger.debug("\t\t- {0}\t{1}".format(task.project.project_name, task.task_number))
    return tasks

def task_update(project_name, task_number, description = None, end_date = None, user = None):
    logger.info("about to update task project_name:{0}, task_number:{1}, description:{2}, end_date:{3}, user: {4}".format(project_name, task_number, description, end_date, user))
    task = task_find(project_name, task_number)
    if task is None:
        raise Exception("not found task to update. Task number:{0} in project:{1}".format(task_number, project_name))
    else:
        if description != None:
            task.description = description
        if end_date != None:
            if end_date == "":
                task.end_date = None
            else:
                task.end_date = end_date
        if user != None:
            if user == "":
                task.user = None
            else:
                task.user = user
        task.save()
        return task

def task_delete(project_name, task_number):
    logger.info("about to delete task number:{0} from project:{1}".format(task_number, project_name))
    project = project_find(project_name)
    if project is None:
        raise Exception("project {0} not Found".format(project_name))
    query = Task.delete().where(Task.project == project and Task.task_number == task_number)
    total_deleted = query.execute()
    logger.info("{0} deleted task".format(total_deleted))
    return total_deleted
