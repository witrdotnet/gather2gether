# Gather2gether

Python project, helps remote people to accomplish tasks together.

# Install

```
pip install gather2gether
```

# Configure

* Start mysql database

```
docker run --rm --name g2gdb -p3307:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=gather2gether -e MYSQL_USER=g2g -e MYSQL_PASSWORD=g2g -d mysql:5.7
```

* Setup gather2gether.properties

Create anywhere configuration file `gather2gether.properties`

```
[database]
host = 127.0.0.1
port = 3307
db_name = gather2gether
user = g2g
password = g2g
```

# Start server

* Configuration file `gather2gether.properties` is created in current directory, run:

```
gather2gether
```

* Configuration file `gather2gether.properties` is created in another directory (suppose /srv/g2g/conf/), run:

```
G2G_CONF_PATH=/srv/g2g/conf gather2gether
```

# Use cli

```
g2g --help
```

# Contribute

## Start gather2gether

```
git clone git@github.com:witrdotnet/gather2gether.git
cd gather2gether/
virtualenv .venv
source .venv/bin/activate
pip install Jinja2
python setup.py install
gather2gether
```
