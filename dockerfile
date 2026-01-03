# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /src

# Copy requirements file and install dependencies
COPY ./src/requirements.txt /src/cyclobots_api/
RUN pip install --no-cache-dir -r /src/cyclobots_api/requirements.txt

# Install debugging utility
RUN pip install debugpy

# Copy the rest of the app code
COPY ./src /src/cyclobots_api

# Set PYTHONPATH to the app directories
ENV PYTHONPATH="/src/cyclobots_api:/src/cyclobots_api"

# Expose the default port
EXPOSE 8080

WORKDIR /src/cyclobots_api

# Run unit tests and then start the API
CMD ["sh", "-c", "python3 -m unittest discover -s tests -p 'test_*.py' && python3 /src/cyclobots_api/main.py || sh"]
