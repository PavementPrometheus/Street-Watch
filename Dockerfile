# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
ADD . /usr/src/app

# Expose our port for accessing the webpages
EXPOSE 4000

# Install any needed packages specified in requirements.txt
# But first make sure pip is up-to-date
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# Run pavementapp.py when the container launches
CMD ["python", "PavementApp/pavementapp.py"]
