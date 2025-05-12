# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
