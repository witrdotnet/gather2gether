import logging
from gather2gether.db import Project

logger = logging.getLogger("g2g-dao-project")

def project_create(project_name, description = None, planned_start_date = None, planned_end_date = None):
    logger.info("about to create project name:{0}, description:{1}, planned_start_date:{2}, planned_end_date:{3}".format(project_name, description, planned_start_date, planned_end_date))
    try:
        project = Project.get(Project.project_name == project_name)
        logger.info("already exists project name:{0}".format(project_name))
        raise Exception("already exists project name:{0}".format(project_name))
    except Project.DoesNotExist:
        project = Project(project_name = project_name, description = description, planned_start_date = planned_start_date, planned_end_date = planned_end_date)
        project.save()
        logger.info("saved new project:{0}".format(project_name))
        return project

def project_find(project_name):
    logger.info("about to find project by name:{0}".format(project_name))
    try:
        project = Project.get(Project.project_name == project_name)
        return project
    except Project.DoesNotExist:
        return None

def project_search(project_name=None, is_closed=None, date=None, date_filter=None, date_operator=None):
    logger.info("about to search project by criteria, project_name:{0}, is_closed:{1}, date:{2}, date_filter:{3}, date_operator:{4}".format(project_name, is_closed, date, date_filter, date_operator))
    clauses = True
    if not project_name is None:
        clauses &= (Project.project_name == project_name)
    if not is_closed is None:
        if is_closed:
            clauses &= (Project.closed_date.is_null(False))
        else:
            clauses &= (Project.closed_date.is_null())
    if not date is None and not date_filter is None and not date_operator is None:
        if date_filter == "start":
            if date_operator == "eq":
                clauses &= (Project.planned_start_date == date)
            elif date_operator == "gt":
                clauses &= (Project.planned_start_date > date)
            elif date_operator == "lt":
                clauses &= (Project.planned_start_date < date)
            elif date_operator == "ge":
                clauses &= (Project.planned_start_date >= date)
            elif date_operator == "le":
                clauses &= (Project.planned_start_date <= date)
        elif date_filter == "end":
            if date_operator == "eq":
                clauses &= (Project.planned_end_date == date)
            elif date_operator == "gt":
                clauses &= (Project.planned_end_date > date)
            elif date_operator == "lt":
                clauses &= (Project.planned_end_date < date)
            elif date_operator == "ge":
                clauses &= (Project.planned_end_date >= date)
            elif date_operator == "le":
                clauses &= (Project.planned_end_date <= date)
        elif date_filter == "close":
            if date_operator == "eq":
                clauses &= (Project.closed_date == date)
            elif date_operator == "gt":
                clauses &= (Project.closed_date > date)
            elif date_operator == "lt":
                clauses &= (Project.closed_date < date)
            elif date_operator == "ge":
                clauses &= (Project.closed_date >= date)
            elif date_operator == "le":
                clauses &= (Project.closed_date <= date)
    projects = Project.select().where(clauses)
    logger.info("found projects by criteria, project_name:{0}, is_closed:{1}, date:{2}, date_filter:{3}, date_operator:{4}".format(project_name, is_closed, date, date_filter, date_operator))
    for project in projects:
        logger.debug("\t\t- {0}\t{1}".format(project.project_name, project.description))
    return projects

def project_update(project_name, new_project_name = None, description = None, planned_start_date = None, planned_end_date = None, closed_date = None):
    logger.info("about to update project name:{0}, description:{1}, planned_start_date:{2}, planned_end_date:{3}, closed_date: {4}".format(project_name, description, planned_start_date, planned_end_date, closed_date))
    try:
        project = Project.get(Project.project_name == project_name)
        if new_project_name != None:
            project.project_name = new_project_name
        if description != None:
            project.description = description
        if planned_start_date != None:
            if planned_start_date == "":
                project.planned_start_date = None
            else:
                project.planned_start_date = planned_start_date
        if planned_end_date != None:
            if planned_end_date == "":
                project.planned_end_date = None
            else:
                project.planned_end_date = planned_end_date
        if closed_date != None:
            if closed_date == "":
                project.closed_date = None
            else:
                project.closed_date = closed_date
        project.save()
        return project
    except Project.DoesNotExist:
        logger.error("not found project to update, project name:{0}".format(project_name))
        raise

def project_delete(project_name):
    logger.info("about to delete project by proect name:{0}".format(project_name))
    query = Project.delete().where(Project.project_name == project_name)
    total_deleted = query.execute()
    logger.info("{0} deleted project".format(total_deleted))
    return total_deleted
