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
  dumphelp
  init      Launch peewee to idempotent initialization of database
```
* g2g db init
```
Usage: g2g db [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dumphelp
  init      Launch peewee to idempotent initialization of database
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
* g2g projects update
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
* g2g projects find
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
* g2g projects search
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
* g2g projects delete
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
* g2g tasks update
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
* g2g tasks find
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
* g2g tasks search
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
* g2g tasks delete
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
* g2g users update
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
* g2g users find
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
* g2g users search
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
* g2g users delete
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
