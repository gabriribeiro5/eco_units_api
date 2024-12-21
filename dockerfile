# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the app code
COPY . .

# Copy the requirements file and install dependencies
COPY src/purePython/requirements.txt src/purePython/
RUN pip install --no-cache-dir -r src/purePython/requirements.txt

# Expose the port your API runs on
EXPOSE 8000

# Command to run your API
CMD ["python", "src/purePython/pureAPI.py"]
