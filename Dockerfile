FROM python:3.8 

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files to the container
COPY app.py .
COPY api.py .
COPY requirements.txt .

RUN pip install --no-cache-dir  -r requirements.txt
# Set the command to run the application
CMD ["python", "app.py"]

# Enable auto-restart for the container
CMD ["python", "api.py", "--host","0.0.0.0","--port","5000"]