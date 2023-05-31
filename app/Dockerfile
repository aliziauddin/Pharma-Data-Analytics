# Base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask server code to the container
COPY . .

# Expose the port on which your Flask server is listening
EXPOSE 5000

# Start the Flask server
CMD [ "python", "server.py" ]
