# eco_units_api
## RESTfull API run on por <8080>
This API collects data from IoT devices (called eco units) and provide them with configuration updates.

Those devices are designed to maintain control over micro-ecosystems, leveraging from sensors (to collect data) and actuators (to interact with their environment).

Foreseeable versions of this API will support human inputs, so they can interact with the database as Customer or Backoffice Agents.

Still, the first and main purpose of this API is to provide eco units with proper support for data management and eventual behavior changes.

## Design
This API leverages from Clean Architecture principles to build a microservice.
Modules are organized as follows:

- **Entities/Interfaces**: Core business rules and models.
    - agent: might be an eco unit, a customer or a backoffice user. They are all agents.
    - agentInput: any database update regarding unit's configuration, self diagnostics or environment state.
    - handler: the base interface for http implementation.\

- **Use Cases**: Application-specific business logic (the actions the application performs).

- **Controllers**: Act as the bridge to handle incoming requests (HTTP requests, API calls, etc.), orchestrating the appropriate use cases and formatting the response.

- **Tests**: Unit tests that must run before the application starts.

- **Utils**: Utilities that enhance flexibility and control over the application.

- **Out of Process (Microservices)**: These can act as external services that are abstracted away from the main application, but which provide critical features like authentication and session management.

## Building Docker Container and Running the Application

### Building with docker-compose (recomended)

To set up and run the API in a Docker container, follow these steps:

0. **Start Docker Engine**
On your terminal, run
```bash
    sudo systemctl start docker
```
or open the **Docker Desktop** application.

1. **Build (or rebuild) the Docker Image**
Open a terminal in the project root directory and execute:  
```bash
    docker-compose up --build
```
The API will now be accessible at http://localhost:8080.

2. **Read logs**
All logs will be written to the /src/eco_units_api/logs.
Use the following command to read log updates in real time:
```bash
    tail -f /src/eco_units_api/logs/purePython.log
```

3. **Stop and Restart for Changes**
To stop the container:
```bash
    docker-compose down
```

To restart with changes:
```bash
    docker-compose up --build
```

### Building with dockerfile only

To set up and run the API in a Docker container, follow these steps:

0. **Start Docker Engine**
On your terminal, run
```bash
    sudo systemctl start docker
```
Or run the Docker Desktop application.

1. **Build the Docker Image**  
Open a terminal in the project root directory and execute:  
```bash
    docker build -t eco_units_api_image:latest .
```

2. **Run the Docker Container**
Start a container from the built image with:
```bash
    docker run -p 8080:8080 eco_units_api_image:latest
```
The API will now be accessible at http://localhost:8080.

4. **Stop the Container**
To stop the running container, press Ctrl+C or use:
```bash
    docker stop <container_id>
```



### Remote Procedure Call (RPC) API runing on port <9090>
(TODO)
