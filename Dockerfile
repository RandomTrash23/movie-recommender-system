FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set the command to run the application
CMD ["python", "app.py"]
