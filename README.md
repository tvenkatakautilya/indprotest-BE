

<h3><b>Install Docker and docker compose</h3>
<h3>CD to the base directory of the repository</h3>
<h3>Run the following command</h3>

```sh
docker-compose up
```

<h3>Commands to toggle admin access to application users</h3>
<h5>Provide admin access to all users</h5>

```sh
docker exec -e PGPASSWORD=postgres -it indprotest-be-db-1 psql -U postgres -d application -c "UPDATE user_authuser SET admin=true;"
```

<h5>Remove admin access to all users</h5>

```sh
docker exec -e PGPASSWORD=postgres -it indprotest-be-db-1 psql -U postgres -d application -c "UPDATE user_authuser SET admin=false;"
```

<h3>Run the following command to stop the application</h3>

```sh
docker-compose down
```

<h2>One time set up</h2>
<h5>Only required to do it for the first time after cloning the repo if the containers are not brought down with out the use of -v flag</h5>

```sh
docker-compose exec web python manage.py migrate
```
