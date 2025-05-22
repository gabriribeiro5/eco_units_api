# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /src

# Copy requirements file and install dependencies
COPY ./src/requirements.txt /src/eco_units_api/
RUN pip install --no-cache-dir -r /src/eco_units_api/requirements.txt

# Install debugging utility
RUN pip install debugpy

# Copy the rest of the app code
COPY ./src /src/eco_units_api

# Set PYTHONPATH to the app directories
ENV PYTHONPATH="/src/eco_units_api:/src/eco_units_api"

# Expose the default port
EXPOSE 8080

WORKDIR /src/eco_units_api

# Run unit tests and then start the API
CMD ["sh", "-c", "python3 -m unittest discover -s tests -p 'test_*.py' && python3 /src/eco_units_api/main.py || sh"]
