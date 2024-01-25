# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /usr/src/app
COPY . /

# Install project dependencies
RUN poetry config virtualenvs.create false \
	&& poetry install --no-interaction --no-ansi

# Command to run the application
CMD ["poetry", "run", "python", "bot"]

