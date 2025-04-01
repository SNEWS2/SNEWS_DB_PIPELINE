FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir poetry
RUN poetry install

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

CMD ["poetry", "run", "python", "src/database/database_connector.py"]