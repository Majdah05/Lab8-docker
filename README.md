# Lab 8 – Docker, containers and images

Majd Aboul Hosn (mga56)

| Folder | What it runs | Port | Image |
| --- | --- | --- | --- |
| `lab5-api/` | Lab 5 – Postman and APIs (users CRUD with SQLite) | 5000 | `mga56/lab8-majd_aboulhosn:0.0.1.RELEASE` |
| `users-api/` | Users API exposing `GET /api/get_users` (names of all users) | 3000 | `mga56/lab8-majd_aboulhosn:0.0.2.RELEASE` |

Docker repository names must be lowercase, so `lab8-Majd_AboulHosn` is written `lab8-majd_aboulhosn`.

## Build the images

Run from this `Lab8` folder with Docker Desktop running:

```bash
docker image build -t mga56/lab8-majd_aboulhosn:0.0.1.RELEASE ./lab5-api
docker image build -t mga56/lab8-majd_aboulhosn:0.0.2.RELEASE ./users-api
```

## Run the containers

```bash
docker run -d -p 5000:5000 --name lab8-api-5000 mga56/lab8-majd_aboulhosn:0.0.1.RELEASE
docker run -d -p 3000:3000 --name lab8-users-3000 mga56/lab8-majd_aboulhosn:0.0.2.RELEASE
```

`-p host:container` maps a port on the machine to the port the app listens on inside the container. Both apps listen on `0.0.0.0`, not `localhost`. If they listened on `localhost`, they would accept connections only from inside the container, and the port mapping would not reach them.

## Try the APIs

- Lab 5 API: <http://localhost:5000/api/users> (plus `GET /api/users/<id>`, `POST /api/users/add`, `PUT /api/users/update`, `DELETE /api/users/delete/<id>`)
- get_users API: <http://localhost:3000/api/get_users> returns, e.g., `["John Doe", "Jane Smith", "Ali Hassan"]`

The port 3000 app adds three sample users when its database is empty. It also accepts `POST /api/users/add` with `name`, `email`, `phone`, `address` and `country` to add more users.

## Activity 1 – commands

| Command | What it does |
| --- | --- |
| `docker ps -a` | Lists all containers, running and stopped, with their ID, image, command, status, ports and name. |
| `docker stop <container>` | Gracefully stops a running container: sends SIGTERM, then SIGKILL after a timeout. The container still exists and can be restarted. |
| `docker logs <container>` | Prints the output (stdout/stderr) the container has produced, e.g. Flask's startup message and request log. |

`stop` and `logs` take a **container** name or ID (from `docker ps -a`), not an image name, e.g. `docker logs lab8-api-5000`.
