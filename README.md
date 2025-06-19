# RoboCore Backend

This repo contains a prototype FastAPI server for managing robotic deployments. It stores data in SQLite via SQLModel and integrates with Portainer and Firebase.

## Configuration

Environment variables can be loaded from a `.env` file. A sample is provided as `.env.example`.
The most important values are:

- `PORTAINER_PORT` - Portainer port (default `8080`)
- `PORTAINER_TOKEN` - API token for Portainer
- `FIREBASE_CREDENTIALS` - Path to Firebase service credentials
- `FIREBASE_TEST_TOKEN` - Optional FCM test device token

## API Highlights

- CRUD operations for Robots, Apps, Hosts and Deployments
- JWT based authentication
- FCM notifications when a deployment is created
- Portainer integration:
  - Pull images on a host: `POST /api/v1/hosts/{host_id}/pull-image`
  - Launch stacks for a deployment: `POST /api/v1/deployments/{deployment_id}/start`
  - Update stack config: `PUT /api/v1/deployments/{deployment_id}/hosts/{host_id}/config`
  - Container control and logs under `/api/v1/containers/*`
  - List containers for hosts, robots, and deployments
  - Exec into a container via `POST /api/v1/containers/{id}/exec`

Run the server with `uvicorn app.main:app --reload`.

## API Endpoints

### Auth
- `POST /api/v1/auth/register` – register a new user
- `POST /api/v1/auth/login` – obtain a JWT token

### Robots
- `GET /api/v1/robots/`
- `POST /api/v1/robots/`
- `GET /api/v1/robots/{robot_id}`
- `PUT /api/v1/robots/{robot_id}`
- `DELETE /api/v1/robots/{robot_id}`
- `GET /api/v1/robots/{robot_id}/containers`

### Apps
- `GET /api/v1/apps/`
- `POST /api/v1/apps/`
- `GET /api/v1/apps/{app_id}`
- `PUT /api/v1/apps/{app_id}`
- `DELETE /api/v1/apps/{app_id}`

### Hosts
- `GET /api/v1/hosts/`
- `POST /api/v1/hosts/`
- `GET /api/v1/hosts/{host_id}`
- `PUT /api/v1/hosts/{host_id}`
- `DELETE /api/v1/hosts/{host_id}`
- `POST /api/v1/hosts/{host_id}/pull-image`
- `GET /api/v1/hosts/{host_id}/containers`

### Deployments
- `GET /api/v1/deployments/`
- `POST /api/v1/deployments/`
- `GET /api/v1/deployments/{dep_id}`
- `DELETE /api/v1/deployments/{dep_id}`
- `POST /api/v1/deployments/{deployment_id}/start`
- `PUT /api/v1/deployments/{deployment_id}/hosts/{host_id}/config`
- `GET /api/v1/deployments/{deployment_id}/containers`

### Notifications
- `POST /api/v1/notifications/send`

### Fleet
- `GET /api/v1/fleet/`
- `POST /api/v1/fleet/deploy`
- `GET /api/v1/fleet/deployments/{deployment_id}`
- `POST /api/v1/fleet/stage`
- `POST /api/v1/fleet/sync`

### Portainer
- `GET /api/v1/portainer/endpoints`
- `GET /api/v1/portainer/endpoints/{endpoint_id}/containers`

### Containers
- `POST /api/v1/containers/{id}/start`
- `POST /api/v1/containers/{id}/stop`
- `GET /api/v1/containers/{id}/logs`
- `GET /api/v1/containers/{id}/stats`
- `POST /api/v1/containers/{id}/exec`

### Introspection
- `GET /api/v1/introspect/{robot_id}/nodes`
- `GET /api/v1/introspect/{robot_id}/topics`
- `WS  /api/v1/introspect/ws/robots/{robot_id}`

### Misc
- `GET /api/v1/health`
