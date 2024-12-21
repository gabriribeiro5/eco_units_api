# eco_units_api
An api that collects data from Eco Units and provide them with behaviour updates to maintain their Ecosystems

## Features

### 1. LogSetup.py
Dynamic Log Directory and File Creation:
    The **createLogDir** method ensures that the specified log directory is created if it doesn't already exist. This is critical for ensuring the logging system works seamlessly without manual intervention.

Configuring the Logging System:
    The **logFileCreateAndConfig** method sets up the basic configuration for logging and writes an initial headline to the log file, showing the calling module that enabled the logger.

Comprehensive Logging Tests:
    The **runTests** method writes test messages to the log file for all log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) to ensure the logger is functioning correctly.

User-Friendly API:
    The **enableLog** method provides a simple interface to initialize logging. It takes in a directory name and a log file name, sets up the directory, configures logging, and runs the tests.

Robust Error Handling:
    Several **try-except blocks** handle exceptions that might occur during directory creation, logging configuration, or file writing.
    
Inspector-Based Calling Module Identification:
    The use of inspect to determine and log the calling module is a nice touch for **traceability and debugging**.

## Design reference
Entities: Core business rules and models.
Use Cases: Application-specific business logic (the actions the application performs).
Interfaces/Controllers: Act as the bridge to handle incoming requests (HTTP requests, API calls, etc.), orchestrating the appropriate use cases and formatting the response.
Out of Process (Microservices): These can act as external services that are abstracted away from the main application, but which provide critical features like authentication and session management.

### Building and Running the Docker Container

To set up and run the API in a Docker container, follow these steps:

1. **Build the Docker Image**  
Open a terminal in the project root directory and execute:  
```bash
    docker build -t eco_units_api:latest .
```

2. **Run the Docker Container**
Start a container from the built image with:
```bash
    docker run -p 8080:8080 eco_units_api:latest
    The API will now be accessible at http://localhost:8080.
```

3. **Stop the Container**
To stop the running container, press Ctrl+C or use:
```bash
    docker stop <container_id>
```

### RESTfull API run on por <8080>

### Remote Procedure Call (RPC) API runing on port <9090>
