# Docker-gather2gether

Dockerized gather2gether.

[Checkout Dockerfile from github](https://github.com/witrdotnet/gather2gether/virt/docker)

# Got docker image

From dockerhub `docker pull witrdotnet/gather2gether`

Or build it yourself

```
docker build -t witrdotnet/gather2gether .
```

# Usage

* An already running database is required

```
docker run --rm --name g2gdb --network g2gnet -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=gather2gether -e MYSQL_USER=g2g -e MYSQL_PASSWORD=g2g -d mysql:5.7
```

* Start gather2gether web server

```
docker run --rm --name g2g   --network g2gnet -p8080:8080 -v $(pwd)/gather2gether.properties:/gather2gether.properties -d witrdotnet/gather2gether
```

* Browse http://localhost:8080

* Manage with g2g CLI

```
docker exec -it g2g g2g users create agent007 "James Bond"
docker exec -it g2g g2g users search
```

[discover more g2g cli commands](../../doc/g2g_cli_doc.md)
