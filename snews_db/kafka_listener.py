import json
import os
import pickle
import random
import sys
import time
from datetime import datetime, timezone
import adc.errors

import click
from hop import Stream

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import Base, AllMessages
from snews_db.db_operations import add_sig_tier_archive, add_time_tier_archive, \
    add_coincidence_tier_archive, add_cached_heartbeats, add_retraction_tier_archive
from snews.models.messages import Tier


class DBKafkaListener:
    def __init__(self, firedrill=False):
        self.observation_topic = os.getenv(
            "FIREDRILL_OBSERVATION_TOPIC" if firedrill else "OBSERVATION_TOPIC"
        )
        self.database_url = os.getenv("DATABASE_URL")
        self.retriable_error_count = 0

    def get_machine_time(self, snews_message):
        if "machine_time" in snews_message.keys():
            return snews_message["machine_time"]
        elif "machine_time_utc" in snews_message.keys():
            return snews_message["machine_time_utc"]
        else:
            raise Exception("No machine time key found in message")
    
    def get_p_val(self, snews_message):
        if snews_message["p_val"] is not None:
            return float(snews_message["p_val"])
        else:
            return None

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
                        
                        # TODO: check if message is a test message, if it is don't add it to the database
                        with SessionLocal() as session:
                            # sort by different types of messages
                            message_tier = snews_message['tier']
                            received_time = str(datetime.now(timezone.utc))
                            if message_tier == Tier.COINCIDENCE_TIER:
                                print("Adding coincidence archive")
                                print(snews_message.keys())
                                add_coincidence_tier_archive(session,
                                                             message_id=snews_message["id"],
                                                             message_uuid=snews_message["uuid"],
                                                             received_time_utc=received_time,
                                                             detector_name=snews_message["detector_name"],
                                                             machine_time_utc=self.get_machine_time(snews_message),
                                                             neutrino_time_utc=snews_message["neutrino_time_utc"],
                                                             p_val=self.get_p_val(snews_message),
                                                             is_test=int(snews_message["is_test"]),
                                                             is_firedrill=int(snews_message["is_firedrill"]))

                            elif message_tier == Tier.SIGNIFICANCE_TIER:
                                print("Adding significance archive")
                                print(snews_message.keys())
                                add_sig_tier_archive(session,
                                                     message_id=snews_message["id"],
                                                     message_uuid=snews_message["uuid"],
                                                     received_time_utc=received_time,
                                                     detector_name=snews_message["detector_name"],
                                                     machine_time_utc=self.get_machine_time(snews_message),
                                                     neutrino_time_utc=snews_message["neutrino_time_utc"],
                                                     p_val=self.get_p_val(snews_message),
                                                     p_values=snews_message["p_values"],
                                                     t_bin_width_sec=float(snews_message["t_bin_width"]),
                                                     is_test=int(snews_message["is_test"]))

                            elif message_tier == Tier.HEART_BEAT:
                                print("Adding heartbeat")
                                print(snews_message.keys())
                                add_cached_heartbeats(session,
                                                      message_id=snews_message["id"],
                                                      message_uuid=snews_message["uuid"],
                                                      received_time_utc=received_time,
                                                      machine_time_utc=self.get_machine_time(snews_message),
                                                      detector_name=snews_message['detector_name'],
                                                      detector_status=snews_message['detector_status'],
                                                      is_test=int(snews_message["is_test"]))

                            elif message_tier == Tier.RETRACTION:
                                print("Adding retraction")
                                print(snews_message.keys())
                                add_retraction_tier_archive(session,
                                                            message_id=snews_message["id"],
                                                            message_uuid=snews_message["uuid"],
                                                            received_time_utc=received_time,
                                                            detector_name=snews_message["detector_name"],
                                                            machine_time_utc=self.get_machine_time(snews_message),
                                                            detector_status=snews_message["detector_status"],
                                                            is_test=int(snews_message["is_test"]))

                            elif message_tier == Tier.TIMING_TIER:
                                print("Adding timing archive")
                                print(snews_message.keys())
                                add_time_tier_archive(session,
                                                      message_id=snews_message["id"],
                                                      message_uuid=snews_message["uuid"],
                                                      received_time_utc=received_time,
                                                      detector_name=snews_message["detector_name"],
                                                      machine_time_utc=self.get_machine_time(snews_message),
                                                      neutrino_time_utc=snews_message["neutrino_time_utc"],
                                                      timing_series=str(snews_message["timing_series"]),
                                                      is_test=int(snews_message["is_test"]))

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

