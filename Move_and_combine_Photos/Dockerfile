# Use the official Python image as the base image
# This image includes Python 3.12 and pip pre-installed
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./skripts ./skripts

#command to run the script
CMD [ "python", "-u", "./skripts/main.py" ]

