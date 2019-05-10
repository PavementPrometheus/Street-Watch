# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Set up the environment
ENV FLASK_APP pavementapp.py
ENV FLASK_RUN_HOST 0.0.0.0

# Expose our port for accessing the webpages. Using the default 5000 port
EXPOSE 5000

# Install any needed packages specified in requirements.txt
# But first make sure pip is up-to-date
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# Run pavementapp.py when the container launches
CMD ["flask", "run"]
