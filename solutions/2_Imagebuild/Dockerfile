# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages using requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the server
EXPOSE 8080

# Run the web server
CMD ["python", "main.py"]