# Use the official Python image as the base image
# This image includes Python 3.12 and pip pre-installed
FROM python:3.12-alpine

# Install Pillow using pip
RUN pip install pillow pillow-heif
# Set the working directory in the container
WORKDIR /app

#command to run the script
CMD [ "python", "-u", "./main.py" ]