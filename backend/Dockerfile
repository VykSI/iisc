# Use official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR .

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the Flask server
CMD ["python", "server.py"]
