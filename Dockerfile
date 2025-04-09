# Use Debian as base image
FROM debian:bullseye-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Python 3 as default
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire project (including app/ structure) into the container
COPY . .

# Expose port 5000 for the app
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Command to run your app
CMD python main.py
