import os
import json
from datetime import datetime

import click
from snews_db.utils import db_utils
from snews_db.database.models import Base
from snews_db.db_operations import write_arbitrary_message
from snews import messages

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


@main.command()
@click.argument('json_file', type=click.Path(exists=True))
def store_message(json_file):
    """Parse a SNEWS message from JSON file and store it in the database"""
    try:
        # Read and parse JSON file
        with open(json_file, 'r') as f:
            message_data = json.load(f)

        # Create messages using snews library
        snews_messages = messages.create_messages(**message_data)

        # Create database session and tables
        db = SessionLocal()
        try:
            # Create all tables if they don't exist
            Base.metadata.create_all(bind=engine)

            # Write each message to the database
            for message in snews_messages:
                # Convert message to dict format expected by write_arbitrary_message
                message_dict = message.model_dump()
                # Add tier information
                message_dict['tier'] = message.tier
                write_arbitrary_message(db, message_dict)
            click.secho("Successfully stored all messages in database", fg="green")
        except Exception as e:
            db.rollback()
            click.secho(f"Error storing messages in database: {str(e)}", fg="red")
        finally:
            db.close()

    except json.JSONDecodeError:
        click.secho("Error: Invalid JSON file", fg="red")
    except Exception as e:
        click.secho(f"Error processing message: {str(e)}", fg="red")


if __name__ == "__main__":
    main()
