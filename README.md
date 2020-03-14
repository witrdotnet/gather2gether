# Gather2gether

Helps remote people to accomplish tasks together.

Gather2gether is composed of a 
* REST api (Flask server)
* CLI ([full documentation](./doc/g2g_cli_doc.md)) 

[![Build Status](https://travis-ci.org/witrdotnet/gather2gether.svg?branch=master)](https://travis-ci.org/witrdotnet/gather2gether)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=witrdotnet_gather2gether&metric=alert_status)](https://sonarcloud.io/dashboard?id=witrdotnet_gather2gether)

# Install

```
pip install gather2gether
```

Alternatives using docker:

* [I prefer start gather2gether inside a docker container](./virt/docker)
* [I prefer start gather2gether with already configured docker compose services](./virt/docker-compose)

# Configure

* Start mysql database

```
docker run --rm --name g2gdb -p3307:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=gather2gether -e MYSQL_USER=g2g -e MYSQL_PASSWORD=g2g -d mysql:5.7
```

* Setup configuration file

Gather2gether will look for configuration file with name `gather2gether.properties` in current directory.

Configuration file content must contain following section:
```
[database]
host = 127.0.0.1
port = 3307
db_name = gather2gether
user = g2g
password = g2g
```

You can use environment variable `G2G_CONF_FILE` to force using different configuration file in any directory.

# Start server

* Run (suppose `gather2gether.properties` file exists in current directory):

```
gather2gether
```

* Or use different configuration file:

```
G2G_CONF_FILE=/path/to/conf/custom.properties gather2gether
```

# Use cli

```
g2g --help
```

# Contribute

## Install from source

```
git clone git@github.com:witrdotnet/gather2gether.git
cd gather2gether/
virtualenv .venv (add "-p /usr/bin/pythonX.Y" to specify python version)
source .venv/bin/activate
pip install Jinja2
python setup.py install
```

## Run Tests

### With unittest

```
python -m unittest discover test/
```

### With nosetests

```
nosetests -v --with-coverage --cover-package=gather2gether --cover-inclusive
```

## Start server

```
gather2gether
```
