# Use Python 3.8 as base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize the database
RUN python init_db.py

# Expose application port
EXPOSE 3111

# Run the application
CMD ["python", "app.py"]

