FROM python:3.11-bullseye

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the project files
COPY . /app
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

## Install dependencies using Poetry
RUN poetry lock
RUN poetry install
RUN poetry run hop auth add hop_creds.csv

CMD ["python", "snews_db/database/kafka_listener.py"]
