import json
import os
import pickle
import random
import sys
import time
from datetime import datetime, timezone
import adc.errors

import click
from snews_db.utils import db_utils
from hop import Stream

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import Base, AllMessages
from snews_db.db_operations import add_sig_tier_archive, add_time_tier_archive, add_coincidence_tier_archive, add_cached_heartbeats, add_retraction_tier_archive 
from snews.models.messages import Tier
from dotenv import load_dotenv
from snews_db.kafka_listener import DBKafkaListener
load_dotenv()


@click.group(invoke_without_command=True)
@click.option(
    "--env",
    type=str,
    default="/tests/etc/test-config.env",
    show_default="/tests/etc/test-config.env",
    help="environment file containing the configurations",
)
@click.pass_context
def main(ctx, env):
    base = os.path.dirname(os.path.realpath(__file__))
    env_path = os.path.join(base, env)
    ctx.ensure_object(dict)
    db_utils.set_env(env_path)
    ctx.obj["env"] = env


@main.command()
@click.option(
    "--firedrill/--no-firedrill",
    default=False,
    show_default="False",
    help="Whether to use firedrill brokers or default ones",
)
def listen_to_detectors(firedrill):
    """Initiate Coincidence Decider"""

    # HOST = gethostname()
    message_runner = DBKafkaListener(firedrill=firedrill)
    try:
        message_runner.run_db_listener()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        click.secho(f'\n{"="*30}DONE{"="*30}', fg="white", bg="green")


if __name__ == "__main__":
    main()
