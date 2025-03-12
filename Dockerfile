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

# Command to run your app
CMD ["python", "main.py"]
ENV FLASK_APP=app
ENV FLASK_ENV=development
