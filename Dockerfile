# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies for Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the NLTK data
RUN python -c "import nltk; nltk.download('punkt')"

# Copy the rest of the application's code into the container at /app
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application
CMD ["python", "TextSummary/manage.py", "runserver", "0.0.0.0:8000"]
