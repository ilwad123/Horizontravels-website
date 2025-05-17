# Use official Python base image
FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy requirements first (helps with Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Run the app
CMD ["python", "PROJECT/app.py"]
