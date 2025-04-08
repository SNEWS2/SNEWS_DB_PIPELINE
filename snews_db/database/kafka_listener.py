import json
import os
import pickle
import random
import sys
import time
from datetime import datetime
import adc.errors

import click
import numpy as np
import pandas as pd
from hop import Stream

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import Base, AllMessages
from snews_db.db_operations import add_all_message
from dotenv import load_dotenv
load_dotenv()

class DBKafkaListener:
    def __init__(self):
        self.observation_topic = os.getenv("FIREDRILL_OBSERVATION_TOPIC")
        self.database_url = os.getenv("DATABASE_URL")
        self.retriable_error_count = 0

    def run_db_listener(self):
        self.retriable_error_count = 0
        while True:
            # create db session
            db_engine = create_engine(self.database_url, echo=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
            Base.metadata.create_all(bind=db_engine)

            stream = Stream(until_eos=False)
            try:
                with stream.open(self.observation_topic, "r") as s:
                    click.secho(
                        f"{datetime.utcnow().isoformat()} (re)Initializing Database Listener System for "
                        f"{self.observation_topic}\n"
                    )
                    for snews_message in s:
                        try:
                            snews_message = snews_message.content
                        except Exception as e:
                            snews_message = snews_message

                        # Unpack the message
                        if type(snews_message) is bytes:
                            snews_message = pickle.loads(snews_message)
                            snews_message = snews_message.model_dump()
                        elif type(snews_message) is str:
                            snews_message = json.loads(snews_message)
                        else:
                            continue

                        # write the message to postgre database
                        with SessionLocal() as session:
                            add_all_message(session, "msg1", "2023-01-01T00:00:00Z", "type1", "This is a test message", "2023-01-02T00:00:00Z")

            except KeyboardInterrupt:
                sys.exit(0)
            except adc.errors.KafkaException as e:
                if e.retriable:
                    self.retriable_error_count += 1
                    if self.retriable_error_count > 10:
                        click.secho(
                            f"{datetime.utcnow().isoformat()} Retriable error count exceeded, exiting...\n"
                        )
                        sys.exit(0)
                    else:
                        time.sleep(
                            (1.5**self.retriable_error_count)
                            * (1 + random.random())
                            / 2
                        )
                else:
                    click.secho(
                        f"{datetime.utcnow().isoformat()} Non-retriable error, exiting...\n"
                    )
                    sys.exit(0)

if __name__ == "__main__":
    listener = DBKafkaListener()
    listener.run_db_listener()
