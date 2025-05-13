import json
import os
import pickle
import random
import sys
import time
from datetime import datetime 
import adc.errors

import click
from hop import Stream

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import Base 
from snews_db.db_operations import write_arbitrary_message

class DBKafkaListener:
    def __init__(self, firedrill=False):
        self.observation_topic = os.getenv(
            "FIREDRILL_OBSERVATION_TOPIC" if firedrill else "OBSERVATION_TOPIC"
        )
        self.database_url = os.getenv("DATABASE_URL")
        self.retriable_error_count = 0

    def run_db_listener(self):
        self.retriable_error_count = 0
        # create db session
        db_engine = create_engine(self.database_url, echo=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        Base.metadata.create_all(bind=db_engine)
        stream = Stream(until_eos=False)
        while True:
            try:
                click.secho(
                    f"{datetime.utcnow().isoformat()} (re)Initializing Database Listener System for "
                    f"{self.observation_topic}\n"
                )
                with stream.open(self.observation_topic, "r") as s:
                    for snews_message in s:
                        try:
                            snews_message = snews_message.content
                        except Exception:
                            pass

                        # Unpack the message
                        try:
                            if isinstance(snews_message, bytes):
                                snews_message = pickle.loads(snews_message)
                                snews_message = snews_message.model_dump()
                            elif isinstance(snews_message, str):
                                snews_message = json.loads(snews_message)
                            else:
                                continue


                            # TODO: check if message is a test message, if it is don't add it to the database
                            with SessionLocal() as session:
                                write_arbitrary_message(session, snews_message)

                        except Exception as e:
                            click.secho(
                                f"{datetime.utcnow().isoformat()} Error processing message: {e}\n",
                                fg="red",
                            )
                            continue  # Skip to the next message

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
                            (1.5 ** self.retriable_error_count)
                            * (1 + random.random())
                            / 2
                        )
                else:
                    click.secho(
                        f"{datetime.utcnow().isoformat()} Non-retriable error, exiting...\n"
                    )
                    sys.exit(0)
            except Exception as e:
                click.secho(
                    f"{datetime.utcnow().isoformat()} Unexpected error: {e}, restarting listener...\n"
                )
                time.sleep(5)  # Add a delay before restarting the listener

