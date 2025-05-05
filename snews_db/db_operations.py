from sqlalchemy.orm import Session
from .database.models import (
    AllMessages,
    SigTierArchive,
    TimeTierArchive,
    CoincidenceTierArchive,
    # CoincidenceTierAlerts, # Assuming this is still commented out or removed
    CachedHeartbeats,
    RetractionTierArchive, # Added import if needed
)
from datetime import datetime # Added import for type hinting if needed
import logging # Added for logging potential errors
from sqlalchemy.ext.declarative import DeclarativeMeta # Import for type hinting model class

# Setup logger
log = logging.getLogger(__name__)

def check_valid_date(date_string: str | None, field_name: str):
    """
    Checks if the input string is a valid ISO 8601 date/datetime string.

    Args:
        date_string: The string to validate. Can be None.
        field_name: The name of the field being checked (for error messages).

    Raises:
        ValueError: If the string is not None and not a valid ISO 8601 format.
    """
    if date_string is None:
        # Allow None if the database schema permits nullable dates
        return
    try:
        # Attempt to parse using ISO 8601 format.
        # Handle potential 'Z' timezone indicator by replacing it.
        datetime.fromisoformat(str(date_string).replace('Z', '+00:00'))
    except (ValueError, TypeError) as e:
        error_message = f"Invalid date string format for field '{field_name}': '{date_string}'. Error: {e}"
        log.error(error_message)
        raise ValueError(error_message) from e

# --- AllMessages ---
def add_all_message(
    session: Session,
    message_id: str,
    received_time: str,
    message_type: str,
    message: str,
    expiration: str,
):
    """Adds a generic message entry."""

    check_valid_date(received_time, "received_time")
    new_message = AllMessages(
        message_id=message_id,
        received_time=received_time,
        message_type=message_type,
        message=message,
        expiration=expiration,
    )
    session.add(new_message)
    session.commit()
    return new_message

# --- SigTierArchive ---
def add_sig_tier_archive(
    session: Session,
    message_id: str,
    message_uuid: str,
    received_time_utc: datetime,
    detector_name: str,
    machine_time_utc: str | None, # Allow None based on schema/usage
    p_val: float | None,
    p_values: str, # Assuming this is a JSON string or similar representation
    t_bin_width_sec: float | None,
    is_test: int,
):
    """Adds a Significance Tier message archive entry."""
    # Example usage: Check date strings before creating the object
    check_valid_date(machine_time_utc, "machine_time_utc")

    new_entry = SigTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc, # Assumed to be a valid datetime object already
        detector_name=detector_name,
        machine_time_utc=machine_time_utc,
        p_val=p_val,
        p_values=p_values,
        t_bin_width_sec=t_bin_width_sec,
        is_test=is_test,
    )
    session.add(new_entry)
    session.commit()
    return new_entry

# --- TimeTierArchive ---
def add_time_tier_archive(
    session: Session,
    message_id: str,
    message_uuid: str,
    received_time_utc: datetime,
    detector_name: str,
    machine_time_utc: str | None,
    neutrino_time_utc: str | None,
    timing_series: str, # Assuming this is a JSON string or similar representation
    is_test: int,
):
    """Adds a Timing Tier message archive entry."""
    check_valid_date(machine_time_utc, "machine_time_utc")
    check_valid_date(neutrino_time_utc, "neutrino_time_utc")

    new_entry = TimeTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc, # Assumed to be a valid datetime object already
        detector_name=detector_name,
        machine_time_utc=machine_time_utc,
        neutrino_time_utc=neutrino_time_utc,
        timing_series=timing_series,
        is_test=is_test,
    )
    session.add(new_entry)
    session.commit()
    return new_entry

# --- CoincidenceTierArchive ---
def add_coincidence_tier_archive(
    session: Session,
    message_id: str,
    message_uuid: str,
    received_time_utc: datetime,
    detector_name: str,
    machine_time_utc: str | None,
    neutrino_time_utc: str | None,
    p_val: float | None,
    is_test: int,
    is_firedrill: int,
):
    """Adds a Coincidence Tier message archive entry."""
    check_valid_date(machine_time_utc, "machine_time_utc")
    check_valid_date(neutrino_time_utc, "neutrino_time_utc")

    new_entry = CoincidenceTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc, # Assumed to be a valid datetime object already
        detector_name=detector_name,
        machine_time_utc=machine_time_utc,
        neutrino_time_utc=neutrino_time_utc,
        p_val=p_val,
        is_test=is_test,
        is_firedrill=is_firedrill,
    )
    session.add(new_entry)
    session.commit()
    return new_entry

# --- CachedHeartbeats ---
def add_cached_heartbeats(
    session: Session,
    message_id: str,
    message_uuid: str,
    received_time_utc: datetime,
    machine_time_utc: str | None, # Changed type hint to datetime, assuming conversion happens before call
    detector_name: str,
    detector_status: str,
    is_test: int,
):
    """Adds a Cached Heartbeat entry."""

    check_valid_date(machine_time_utc, "machine_time_utc")
    new_entry = CachedHeartbeats(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc, # Assumed to be a valid datetime object already
        machine_time=machine_time_utc, # Pass the datetime object or None
        detector_name=detector_name,
        detector_status=detector_status,
        is_test=is_test,
    )
    session.add(new_entry)
    session.commit()
    return new_entry

# --- RetractionTierArchive ---
def add_retraction_tier_archive(
    session: Session,
    message_id: str,
    message_uuid: str,
    received_time_utc: datetime,
    detector_name: str,
    machine_time_utc: str | None,
    detector_status: str,
    is_test: int,
):
    """Adds a Retraction Tier message archive entry."""
    check_valid_date(machine_time_utc, "machine_time_utc")

    new_entry = RetractionTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc, # Assumed to be a valid datetime object already
        detector_name=detector_name,
        machine_time_utc=machine_time_utc,
        detector_status=detector_status,
        is_test=is_test,
    )
    session.add(new_entry)
    session.commit()
    return new_entry

# --- Generic Delete Operation ---
def delete_all_from_table(session: Session, model_class: DeclarativeMeta):
    """
    Deletes all rows from the specified table model.

    Args:
        session: The SQLAlchemy session object.
        model_class: The SQLAlchemy model class representing the table
                     (e.g., AllMessages, CachedHeartbeats).

    Returns:
        The number of rows deleted.
    """
    try:
        num_rows_deleted = session.query(model_class).delete()
        session.commit()
        log.info(f"Deleted {num_rows_deleted} rows from {model_class.__tablename__}")
        return num_rows_deleted
    except Exception as e:
        session.rollback() # Rollback in case of error
        log.error(f"Error deleting rows from {model_class.__tablename__}: {e}")
        raise # Re-raise the exception after logging and rollback
