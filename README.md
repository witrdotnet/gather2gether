# Gather2gether

Helps remote people to accomplish tasks together.

Gather2gether is composed of a 
* REST api (Flask server)
* CLI ([full documentation](./doc/g2g_cli_doc.md)) 

[![Build Status](https://travis-ci.com/witrdotnet/gather2gether.svg?branch=master)](https://travis-ci.com/witrdotnet/gather2gether)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=witrdotnet_gather2gether&metric=alert_status)](https://sonarcloud.io/dashboard?id=witrdotnet_gather2gether)

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

## Install from source

```
git clone git@github.com:witrdotnet/gather2gether.git
cd gather2gether/
virtualenv .venv
source .venv/bin/activate
pip install Jinja2
python setup.py install
```

## Run Tests

```
python -m unittest discover test/
```

## Start server

```
gather2gether
```
