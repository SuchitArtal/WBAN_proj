# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including app/ structure) into the container
COPY . .

# Expose port 5000 for the app
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Create a startup script
RUN echo '#!/bin/bash\npython init_db.py\npython main.py' > /app/start.sh
RUN chmod +x /app/start.sh

# Command to run your app
CMD ["/app/start.sh"]
