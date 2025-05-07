import pytest
import subprocess
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import (
    Base, CoincidenceTierArchive, TimeTierArchive,
    SigTierArchive, CachedHeartbeats, RetractionTierArchive
)

DATABASE_URL = "postgresql://user:password@localhost:5433/snews_pg"
SNEWS_DB_ROOT = Path(__file__).parent.parent.parent

@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope="module")
def session_factory(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def run_store_command(message_filename):
    message_path = SNEWS_DB_ROOT / "snews_db/tests/example_messages" / message_filename
    print(f"\nAttempting to store message from: {message_path}")
    result = subprocess.run(
        ["snews_db", "store-message", str(message_path)],
        cwd=SNEWS_DB_ROOT,
        capture_output=True,
        text=True,
        check=False
    )
    if result.returncode != 0:
        print("snews_db store-message command failed:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    result.check_returncode()

def test_store_heartbeat_message(session_factory):
    """Test storing a heartbeat message"""
    run_store_command("example_heartbeat_message.json")
    session = session_factory()
    try:
        heartbeat_messages = session.query(CachedHeartbeats).all()
        assert len(heartbeat_messages) > 0, "No heartbeat messages found in database"
        latest_message = heartbeat_messages[-1]
        assert latest_message.detector_name == "DS-20K"
        assert latest_message.detector_status == "OFF"
        assert latest_message.is_test == 1
    finally:
        session.close()

def test_store_significance_message(session_factory):
    """Test storing a significance tier message"""
    run_store_command("example_significance_tier_message.json")
    session = session_factory()
    try:
        sig_messages = session.query(SigTierArchive).all()
        assert len(sig_messages) > 0, "No significance tier messages found in database"
        latest_message = sig_messages[-1]
        assert latest_message.detector_name == "KamLAND"
        assert latest_message.p_val == 0.05
        assert latest_message.is_test == 1
    finally:
        session.close()

def test_store_timing_message(session_factory):
    """Test storing a timing tier message"""
    run_store_command("example_timing_tier_message.json")
    session = session_factory()
    try:
        timing_messages = session.query(TimeTierArchive).all()
        assert len(timing_messages) > 0, "No timing tier messages found in database"
        latest_message = timing_messages[-1]
        assert latest_message.detector_name == "IceCube"
        assert latest_message.is_test == 1
    finally:
        session.close()

def test_store_coincidence_message(session_factory):
    """Test storing a coincidence tier message"""
    run_store_command("example_coincidence_tier_message.json")
    session = session_factory()
    try:
        coincidence_messages = session.query(CoincidenceTierArchive).all()
        assert len(coincidence_messages) > 0, "No coincidence tier messages found in database"
        latest_message = coincidence_messages[-1]
        assert latest_message.detector_name == "XENONnT"
        assert latest_message.p_val == 0.07
        assert latest_message.is_test == 1
    finally:
        session.close()

def test_store_combined_message(session_factory):
    """Test storing a combined message with multiple tiers"""
    run_store_command("example_combined_message.json")
    session = session_factory()
    try:
        # Check that messages were stored in appropriate tables
        sig_messages = session.query(SigTierArchive).all()
        timing_messages = session.query(TimeTierArchive).all()
        coincidence_messages = session.query(CoincidenceTierArchive).all()
        
        assert len(sig_messages) > 0, "No significance tier messages found in database"
        assert len(timing_messages) > 0, "No timing tier messages found in database"
        assert len(coincidence_messages) > 0, "No coincidence tier messages found in database"
    finally:
        session.close() 