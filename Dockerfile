# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app
COPY run.py ./

# Expose port
EXPOSE 8000

# Run the Flask app
CMD ["python", "run.py"]