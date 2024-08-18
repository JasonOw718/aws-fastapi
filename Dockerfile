# Use an official Python runtime as a parent image
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /opt/render/project/src

# Copy the current directory contents into the container at /opt/render/project/src
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader wordnet -d /opt/render/project/src/nltk_data

# Make port 80 available to the world outside this container (or whichever port your FastAPI app runs on)
EXPOSE 80

# Define environment variable
ENV NLTK_DATA=/opt/render/project/src/nltk_data

# Command to run the FastAPI application using Uvicorn, with automatic reloading enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
