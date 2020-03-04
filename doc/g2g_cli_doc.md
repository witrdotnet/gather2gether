# Gather2gether cli documentation
## All main commands
```
Usage: g2g [OPTIONS] COMMAND [ARGS]...

  Management script for gather2gether application.

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  db
  projects
  routes    Show the routes for the app.
  run       Run a development server.
  shell     Run a shell in the app context.
  tasks
  users
```
## g2g db
```
Usage: g2g db [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init  Launch peewee to idempotent initialization of database
```
* g2g db init
```
Usage: g2g db init [OPTIONS]

  Launch peewee to idempotent initialization of database

Options:
  --help  Show this message and exit.
```
## g2g projects
```
Usage: g2g projects [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Creates new project
  delete  Delete project with provided name.
  find    Find project by its name.
  search  Search projects by criteria.
  update  Updates existing project
```
* g2g projects create
```
Usage: g2g projects create [OPTIONS] PROJECT_NAME

  Creates new project

Options:
  --description TEXT
  --planned_start_date TEXT
  --planned_end_date TEXT
  --help                     Show this message and exit.
```
* g2g projects update
```
Usage: g2g projects update [OPTIONS] PROJECT_NAME

  Updates existing project

Options:
  --new_project_name TEXT
  --description TEXT
  --planned_start_date TEXT
  --planned_end_date TEXT
  --closed_date TEXT
  --help                     Show this message and exit.
```
* g2g projects find
```
Usage: g2g projects find [OPTIONS] PROJECT_NAME

  Find project by its name. Returns one project or None

Options:
  --help  Show this message and exit.
```
* g2g projects search
```
Usage: g2g projects search [OPTIONS]

  Search projects by criteria. Returns list of projects

Options:
  --project_name TEXT
  --is_closed BOOLEAN
  --date TEXT
  --date_filter [start|end|close]
  --date_operator [eq|lt|gt|le|ge]
  --help                          Show this message and exit.
```
* g2g projects delete
```
Usage: g2g projects delete [OPTIONS] PROJECT_NAME

  Delete project with provided name. Returns total deleted projects

Options:
  --help  Show this message and exit.
```
## g2g tasks
```
Usage: g2g tasks [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Creates new task
  delete  Delete task with provided task number and project name.
  find    Find task by project name and task number.
  search  Search tasks by criteria.
  update  Updates existing task
```
* g2g tasks create
```
Usage: g2g tasks create [OPTIONS] PROJECT_NAME TASK_NUMBER

  Creates new task

Options:
  --description TEXT
  --help              Show this message and exit.
```
* g2g tasks update
```
Usage: g2g tasks update [OPTIONS] PROJECT_NAME TASK_NUMBER

  Updates existing task

Options:
  --description TEXT
  --end_date TEXT
  --user_external_id TEXT
  --help                   Show this message and exit.
```
* g2g tasks find
```
Usage: g2g tasks find [OPTIONS] PROJECT_NAME TASK_NUMBER

  Find task by project name and task number. Returns one task or None

Options:
  --help  Show this message and exit.
```
* g2g tasks search
```
Usage: g2g tasks search [OPTIONS]

  Search tasks by criteria. Returns list of tasks

Options:
  --project_name TEXT
  --task_number TEXT
  --is_closed BOOLEAN
  --end_date TEXT
  --date_operator [eq|lt|gt|le|ge]
  --user_external_id TEXT
  --help                          Show this message and exit.
```
* g2g tasks delete
```
Usage: g2g tasks delete [OPTIONS] PROJECT_NAME TASK_NUMBER

  Delete task with provided task number and project name. Returns total
  deleted tasks

Options:
  --help  Show this message and exit.
```
## g2g users
```
Usage: g2g users [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create  Creates new user
  delete  Delete user with provided external id.
  find    Find user by its external id.
  search  Search users by criteria.
  update  Updates existing user
```
* g2g users create
```
Usage: g2g users create [OPTIONS] EXTERNAL_ID NAME

  Creates new user

Options:
  --help  Show this message and exit.
```
* g2g users update
```
Usage: g2g users update [OPTIONS] EXTERNAL_ID

  Updates existing user

Options:
  --name TEXT
  --active BOOLEAN
  --help            Show this message and exit.
```
* g2g users find
```
Usage: g2g users find [OPTIONS] EXTERNAL_ID

  Find user by its external id. Returns one user or None

Options:
  --help  Show this message and exit.
```
* g2g users search
```
Usage: g2g users search [OPTIONS]

  Search users by criteria. Returns list of users

Options:
  --external_id TEXT
  --name TEXT
  --active BOOLEAN
  --help              Show this message and exit.
```
* g2g users delete
```
Usage: g2g users delete [OPTIONS] EXTERNAL_ID

  Delete user with provided external id. Returns total deleted users

Options:
  --help  Show this message and exit.
```
