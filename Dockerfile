# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files to the container
COPY . .

# Run the main app
CMD ["python", "main.py"]
