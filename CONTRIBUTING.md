## Testing and debugging

### Runing the application iteractivelly
In order to access the container iteractive shell, you may choose between one of the following options:

1. **Use Docker-Compose to build (or rebuild) the image**
Open the **Docker Desktop** application.
Then open a terminal in the project root directory and execute:
```bash
    docker-compose up --build
```
Execute interactive commands using Docker Desktop

2. **Iteractively run a single container**
On a new terminal, run the following:
```bash
    docker run -p 8080:8080 -iteractive eco_units_api_image:latest
```

3. **Accessing Docker container after running it**
On a new terminal, run the following:
```bash
    docker exec -it eco_units_api_container /bin/sh
```

### Talking to the applicationIn
Understand and manipulate the application using one (or a combination) of the following options:

1. **Reading logs**
All logs will be written to `/var/log/eco_units_api`.
Use the following command to read log updates in real time:
```bash
    tail -f /var/log/eco_units_api/purePython.log
```

[Tip]: If docker-compose is being used, iteractive shell is not necessary.
Due to mount bindings on docker-compose.yml, you should be able to read from `./eco_units_api/logs/purePython.log` directly on your OS file system.

2. **Editing files** 
By default, the docker image does not have any editor installed.
To apply any experimental change without having to rebuild the app,
Run the iteractive shell (option 1 or 2), and then run:
```bash
    apt update
    apt install vim
```

[Tip]: If docker-compose is being used, iteractive shell is not necessary.
Due to mount bindings on docker-compose.yml, you should be able to update files at `./src` directly on your OS file system.

### Testing the application
Here are some options on how to 
test the application routes:

1. **Unit tests**
Run the iteractive shell (option 1 or 2), and then run:
```bash
    python3 -m unittest discover -s tests -p 'test_*.py'
```

2. **Testing routes and methods** 
On **Bash** or **CMD**:
```bash
    curl -v -X TRACE http://localhost:8080/pureAPI
```

On **PowerShell**, use native method:
```bash
    Invoke-WebRequest -Uri http://localhost:8080/pureAPI -Method TRACE -Verbose
```
or run the actual curl file:
```bash
    & "C:\path\to\curl.exe" -v -X TRACE http://localhost:8080/pureAPI
```
On **Wsl**:
```bash
    sudo apt update && sudo apt install curl
    curl -v -X TRACE http://localhost:8080/pureAPI
```