import pytest
import subprocess
import time
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import (
    Base, AllMessages, CoincidenceTierArchive, TimeTierArchive,
    SigTierArchive, CachedHeartbeats
)
from datetime import datetime, timezone
import os

DATABASE_URL = "postgresql://user:password@localhost:5433/snews_pg"
SNEWS_DB_ROOT = Path(__file__).parent.parent.parent

@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope="module")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def session_factory(engine, tables):
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal

@pytest.fixture(scope="module")
def kafka_listener():
    listener_logfile_out = SNEWS_DB_ROOT / "listener_stdout.log"
    listener_logfile_err = SNEWS_DB_ROOT / "listener_stderr.log"
    with open(listener_logfile_out, "wb") as f_out, open(listener_logfile_err, "wb") as f_err:
        proc = subprocess.Popen(
            ["snews_db", "listen-to-detectors", "--firedrill"],
            stdout=f_out,
            stderr=f_err,
            cwd=SNEWS_DB_ROOT
        )
    initial_wait = 5
    print(f"\nWaiting {initial_wait}s for Kafka listener to initialize...")
    time.sleep(initial_wait)

    poll_result = proc.poll()
    if poll_result is not None:
        pytest.fail(f"Kafka listener process terminated prematurely with exit code {poll_result}. Check logs.")
    else:
        print("Kafka listener process appears to be running.")

    yield

    print("Terminating Kafka listener process...")
    proc.terminate()
    try:
        proc.wait(timeout=5)
        print("Kafka listener process terminated.")
    except subprocess.TimeoutExpired:
        print("Kafka listener process did not terminate gracefully, killing.")
        proc.kill()
        proc.wait()

def run_publish_command(message_filename):
    message_path = SNEWS_DB_ROOT / "snews_db/tests/example_messages" / message_filename
    print(f"\nAttempting to publish message from: {message_path}")
    result = subprocess.run(
        ["snews_pt", "publish", str(message_path), "--firedrill"],
        cwd=SNEWS_DB_ROOT,
        capture_output=True,
        text=True,
        check=False
    )
    if result.returncode != 0:
        print("snews_pt publish command failed:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    result.check_returncode()
    time.sleep(5)

def test_coincidence_message(kafka_listener, session_factory):
    run_publish_command("example_coincidence_tier_message.json")
    session = session_factory()
    try:
        coincidence_messages = session.query(CoincidenceTierArchive).all()
        assert len(coincidence_messages) == 1, f"Expected 1 message, but found {len(coincidence_messages)} in CoincidenceTierArchive table."
        assert coincidence_messages[0].detector_name == "XENONnT"
        assert coincidence_messages[0].p_val == 0.07
    finally:
        session.close()

def test_timing_message(kafka_listener, session_factory):
    run_publish_command("example_timing_tier_message.json")
    session = session_factory()
    try:
        timing_messages = session.query(TimeTierArchive).all()
        assert len(timing_messages) == 1, f"Expected 1 message, but found {len(timing_messages)} in TimeTierArchive table."
        assert timing_messages[0].detector_name == "IceCube"
    finally:
        session.close()

def test_significance_message(kafka_listener, session_factory):
    run_publish_command("example_significance_tier_message.json")
    session = session_factory()
    try:
        sig_messages = session.query(SigTierArchive).all()
        assert len(sig_messages) == 1, f"Expected 1 message, but found {len(sig_messages)} in SigTierArchive table."
        assert sig_messages[0].detector_name == "KamLAND"
        assert sig_messages[0].p_val == 0.05
    finally:
        session.close()

def test_heartbeat_message(kafka_listener, session_factory):
    run_publish_command("example_heartbeat_message.json")
    session = session_factory()
    try:
        hb_messages = session.query(CachedHeartbeats).all()
        found = any("DS-20K" in msg.detector_name for msg in hb_messages)
        assert found, "Expected heartbeat message from DS-20K not found in CachedHeartbeats table."
    finally:
        session.close()
