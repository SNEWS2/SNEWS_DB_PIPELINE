import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import (
    Base, AllMessages, SigTierArchive, TimeTierArchive,
    CoincidenceTierArchive, CachedHeartbeats, RetractionTierArchive
)
from snews_db.db_operations import (
    add_all_message, add_sig_tier_archive, add_time_tier_archive,
    add_coincidence_tier_archive, add_cached_heartbeats, add_retraction_tier_archive
)
from datetime import datetime, timezone

DATABASE_URL = "postgresql://user:password@localhost:5433/snews_pg"
@pytest.fixture(scope='module')
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    """Creates a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_add_all_message(session):
    message = add_all_message(session, "msg1", "2023-01-01T00:00:00Z", "type1", "This is a test message", "2023-01-02T00:00:00Z")
    assert message.id is not None
    assert message.message_id == "msg1"
    assert message.received_time == "2023-01-01T00:00:00Z"
    assert message.message_type == "type1"
    assert message.message == "This is a test message"
    assert message.expiration == "2023-01-02T00:00:00Z"

    # Verify that the record was created in the database
    db_message = session.query(AllMessages).filter_by(message_id="msg1").first()
    assert db_message is not None
    assert db_message.message_id == "msg1"
    assert db_message.received_time == "2023-01-01T00:00:00Z"
    assert db_message.message_type == "type1"
    assert db_message.message == "This is a test message"
    assert db_message.expiration == "2023-01-02T00:00:00Z"

def test_add_all_message_invalid(session):
    # Test adding a message with invalid data
    with pytest.raises(Exception):
        # invalid date
        add_all_message(session, "msg1", "this is an invalid date", "type1", "This is a test message", "2023-01-02T00:00:00Z") 

def test_add_sig_tier_archive_full(session):
    """Test adding SigTierArchive with all fields."""
    now = datetime.now(timezone.utc)
    machine_time_str = "2023-01-01T00:00:05Z"
    neutrino_time_str = "2023-01-01T00:00:00Z"
    entry = add_sig_tier_archive(
        session, "sig1", "uuid-sig1", now, "DetectorA", machine_time_str,
        neutrino_time_str, 0.05, '{"val": 1}', 0.1, 0
    )
    assert entry.id is not None
    assert entry.message_id == "sig1"
    assert entry.message_uuid == "uuid-sig1"
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.detector_name == "DetectorA"
    assert entry.machine_time_utc == machine_time_str
    assert entry.neutrino_time_utc == neutrino_time_str
    assert entry.p_val == 0.05
    assert entry.p_values == '{"val": 1}'
    assert entry.t_bin_width_sec == 0.1
    assert entry.is_test == 0

    db_entry = session.query(SigTierArchive).filter_by(message_id="sig1").first()
    assert db_entry is not None
    assert db_entry.machine_time_utc == machine_time_str
    assert db_entry.neutrino_time_utc == neutrino_time_str

def test_add_time_tier_archive_no_machine_time(session):
    """Test adding TimeTierArchive with null machine time."""
    now = datetime.now(timezone.utc)
    neutrino_time_str = "2023-01-02T11:00:00Z"
    entry = add_time_tier_archive(
        session, "time2", "uuid-time2", now, "DetectorD", None,
        neutrino_time_str, '[]', 1
    )
    assert entry.id is not None
    assert entry.message_id == "time2"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.machine_time_utc is None
    assert entry.neutrino_time_utc == neutrino_time_str

    db_entry = session.query(TimeTierArchive).filter_by(message_id="time2").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert db_entry.machine_time_utc is None

# --- CoincidenceTierArchive Tests ---

def test_add_coincidence_tier_archive_full(session):
    """Test adding CoincidenceTierArchive with all fields."""
    now = datetime.now(timezone.utc)
    machine_time_str = "2023-01-03T12:00:05Z"
    neutrino_time_str = "2023-01-03T12:00:00Z"
    entry = add_coincidence_tier_archive(
        session, "coinc1", "uuid-coinc1", now, "DetectorE", machine_time_str,
        neutrino_time_str, 0.01, 0, 1
    )
    assert entry.id is not None
    assert entry.message_id == "coinc1"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.machine_time_utc == machine_time_str
    assert entry.neutrino_time_utc == neutrino_time_str
    assert entry.p_val == 0.01
    assert entry.is_firedrill == 1

    db_entry = session.query(CoincidenceTierArchive).filter_by(message_id="coinc1").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert db_entry.machine_time_utc == machine_time_str
    assert db_entry.neutrino_time_utc == neutrino_time_str

def test_add_coincidence_tier_archive_no_times_no_pval(session):
    """Test adding CoincidenceTierArchive with null times and p_val."""
    now = datetime.now(timezone.utc)
    entry = add_coincidence_tier_archive(
        session, "coinc2", "uuid-coinc2", now, "DetectorF", None, None, None, 1, 0
    )
    assert entry.id is not None
    assert entry.message_id == "coinc2"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.machine_time_utc is None
    assert entry.neutrino_time_utc is None
    assert entry.p_val is None
    assert entry.is_test == 1

    db_entry = session.query(CoincidenceTierArchive).filter_by(message_id="coinc2").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert db_entry.machine_time_utc is None
    assert db_entry.neutrino_time_utc is None

# --- CachedHeartbeats Tests ---

def test_add_cached_heartbeats_full(session):
    """Test adding CachedHeartbeats with all fields."""
    now = datetime.now(timezone.utc)
    machine_time_str_input = "2023-01-04T14:00:00Z" # The input string format
    entry = add_cached_heartbeats(
        session, "hb1", "uuid-hb1", now, machine_time_str_input, "DetectorG", "ON", 0
    )
    assert entry.id is not None
    assert entry.message_id == "hb1"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now

    # --- Compare machine_time ---
    # Parse the expected string into a datetime object (handle 'Z')
    expected_dt = datetime.fromisoformat(machine_time_str_input.replace('Z', '+00:00'))
    # Assuming entry.machine_time is a naive datetime object representing UTC
    # Make it timezone-aware before comparing
    actual_dt_aware = entry.machine_time.replace(tzinfo=timezone.utc)
    # Compare the datetime objects
    assert actual_dt_aware == expected_dt
    # --- End Compare machine_time ---

    assert entry.detector_status == "ON"

    db_entry = session.query(CachedHeartbeats).filter_by(message_id="hb1").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now

    # --- Compare machine_time from DB query ---
    # Parse the expected string
    expected_dt_db = datetime.fromisoformat(machine_time_str_input.replace('Z', '+00:00'))
    # Assuming db_entry.machine_time is a naive datetime object representing UTC
    # Make it timezone-aware before comparing
    actual_dt_db_aware = db_entry.machine_time.replace(tzinfo=timezone.utc)
    # Compare the datetime objects
    assert actual_dt_db_aware == expected_dt_db

def test_add_cached_heartbeats_no_machine_time(session):
    """Test adding CachedHeartbeats with null machine time."""
    now = datetime.now(timezone.utc)
    entry = add_cached_heartbeats(
        session, "hb2", "uuid-hb2", now, None, "DetectorH", "OFF", 1
    )
    assert entry.id is not None
    assert entry.message_id == "hb2"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.machine_time is None
    assert entry.detector_status == "OFF"

    db_entry = session.query(CachedHeartbeats).filter_by(message_id="hb2").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert db_entry.machine_time is None

# --- RetractionTierArchive Tests ---

def test_add_retraction_tier_archive_full(session):
    """Test adding RetractionTierArchive with all fields."""
    now = datetime.now(timezone.utc)
    machine_time_str = "2023-01-05T16:00:05Z"
    entry = add_retraction_tier_archive(
        session, "ret1", "uuid-ret1", now, "DetectorI", machine_time_str, "RETRACTED", 0
    )
    assert entry.id is not None
    assert entry.message_id == "ret1"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.machine_time_utc == machine_time_str
    assert entry.detector_status == "RETRACTED"

    db_entry = session.query(RetractionTierArchive).filter_by(message_id="ret1").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert db_entry.machine_time_utc == machine_time_str

def test_add_retraction_tier_archive_no_machine_time(session):
    """Test adding RetractionTierArchive with null machine time."""
    now = datetime.now(timezone.utc)
    entry = add_retraction_tier_archive(
        session, "ret2", "uuid-ret2", now, "DetectorJ", None, "RETRACTED", 1
    )
    assert entry.id is not None
    assert entry.message_id == "ret2"
    # Make naive datetime aware before comparing
    assert entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert entry.machine_time_utc is None

    db_entry = session.query(RetractionTierArchive).filter_by(message_id="ret2").first()
    assert db_entry is not None
    # Make naive datetime aware before comparing
    assert db_entry.received_time_utc.replace(tzinfo=timezone.utc) == now
    assert db_entry.machine_time_utc is None

# --- Invalid Date Tests ---

def test_add_sig_tier_archive_invalid_date(session):
    """Test adding SigTierArchive with invalid date string."""
    now = datetime.now(timezone.utc)
    # Assuming check_valid_date raises "Invalid isoformat string: 'not-a-date'"
    with pytest.raises(ValueError, match=r"Invalid isoformat string:.*'not-a-date'"):
        add_sig_tier_archive(
            session, "sig_invalid", "uuid-sig_invalid", now, "DetectorX", "not-a-date",
            "2023-01-01T00:00:00Z", 0.05, '[]', 0.1, 0
        )

def test_add_time_tier_archive_invalid_date(session):
    """Test adding TimeTierArchive with invalid date string."""
    now = datetime.now(timezone.utc)
    # Update the match parameter to expect the actual error message from fromisoformat
    with pytest.raises(ValueError, match=r"Invalid isoformat string:.*'bad-date'"):
        add_time_tier_archive(
            session, "time_invalid", "uuid-time_invalid", now, "DetectorY", "2023-01-01T00:00:05Z",
            "bad-date", '[]', 0
        )
