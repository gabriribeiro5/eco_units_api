# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /src

# Copy the app code
COPY . .

# Copy the requirements file and install dependencies
COPY src/purePython/requirements.txt src/purePython/
RUN pip install --no-cache-dir -r src/purePython/requirements.txt

# Expose the port your API runs on
EXPOSE 8080

# Use a shell environment to run unit tests and the API
CMD ["/bin/sh", "-c", "python3 -m unittest discover -s src/purePython/tests/ && python3 src/purePython/pureAPI.py"]
