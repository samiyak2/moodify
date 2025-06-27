# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable to suppress Python warnings
ENV PYTHONUNBUFFERED True

# Expose the port Flask will run on
ENV PORT 8080

# Run the app
CMD ["python", "app.py"]