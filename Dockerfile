# Using slim python 3.8 container
FROM python:3.8-slim

COPY requirements.txt ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install make
RUN apt-get update && apt-get install make

# Install sphinx
RUN apt-get -y install python3-sphinx

# Set working directory
WORKDIR /usr/who_clean

# Copy all files to container
COPY . .
