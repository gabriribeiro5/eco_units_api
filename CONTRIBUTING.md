## Testing and debugging

0. **Iteractively run**
On a new terminal, run the following:
```bash
    docker run -p 8080:8080 -iteractive eco_units_api_image:latest
```

1. **Accessing Docker Container after running it**
On a new terminal, run the following:
```bash
    docker exec -it eco_units_api_container /bin/sh
```

2. **Reading logs**
All logs will be written to the /src/eco_units_api/logs.
Use the following command to read log updates in real time:
```bash
    tail -f /src/eco_units_api/logs/purePython.log
```

3. **Editing files iteractive** 
By default, the docker image does not have any editor installed.
To apply any experimental change without having to rebuild the app,
Run the iteractive shell (option 1 or 2), and then run:
```bash
    apt update
    apt install vim
```

4. **Testing routes and methods** 
On Bash or CMD:
```bash
    curl -v -X TRACE http://localhost:8080/pureAPI
```

On PowerShell, use native method:
```bash
    Invoke-WebRequest -Uri http://localhost:8080/pureAPI -Method TRACE -Verbose
```
or run the actual curl file:
```bash
    & "C:\path\to\curl.exe" -v -X TRACE http://localhost:8080/pureAPI
```
On Wsl:
```bash
    sudo apt update && sudo apt install curl
    curl -v -X TRACE http://localhost:8080/pureAPI
```