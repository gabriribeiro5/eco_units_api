# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /src

# Copy requirements file and install dependencies
COPY ./src/purePython/requirements.txt /src/eco_units_api/src/purePython/
RUN pip install --no-cache-dir -r /src/eco_units_api/src/purePython/requirements.txt

# Copy the rest of the app code
COPY ./src /src/eco_units_api/src

# Set PYTHONPATH to the app directories
ENV PYTHONPATH="/src/eco_units_api/src:/src/eco_units_api/src/purePython"

# Expose the default port
EXPOSE 8080

WORKDIR /src/eco_units_api/src/purePython

# Run unit tests and then start the API
CMD ["sh", "-c", "python3 -m unittest discover -s tests -p 'test_*.py' && python3 /src/eco_units_api/src/purePython/pureAPI.py || sh"]

