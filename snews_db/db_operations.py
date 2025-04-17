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
    machine_time_utc: str,
    neutrino_time_utc: str,
    p_val: float,
    p_values: str, # Assuming this is a JSON string or similar representation
    t_bin_width_sec: float,
    is_test: int,
):
    """Adds a Significance Tier message archive entry."""
    new_entry = SigTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc,
        detector_name=detector_name,
        machine_time_utc=machine_time_utc,
        neutrino_time_utc=neutrino_time_utc,
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
    machine_time_utc: str,
    neutrino_time_utc: str,
    timing_series: str, # Assuming this is a JSON string or similar representation
    is_test: int,
):
    """Adds a Timing Tier message archive entry."""
    new_entry = TimeTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc,
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
    machine_time_utc: str,
    neutrino_time_utc: str,
    p_val: float,
    is_test: int,
    is_firedrill: int,
):
    """Adds a Coincidence Tier message archive entry."""
    new_entry = CoincidenceTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc,
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
    machine_time_utc: datetime,
    detector_name: str,
    detector_status: str,
    is_test: int,
):
    """Adds a Cached Heartbeat entry."""
    new_entry = CachedHeartbeats(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc,
        machine_time=machine_time_utc,
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
    machine_time_utc: str,
    detector_status: str,
    is_test: int,
):
    """Adds a Retraction Tier message archive entry."""
    new_entry = RetractionTierArchive(
        message_id=message_id,
        message_uuid=message_uuid,
        received_time_utc=received_time_utc,
        detector_name=detector_name,
        machine_time_utc=machine_time_utc,
        detector_status=detector_status,
        is_test=is_test,
    )
    session.add(new_entry)
    session.commit()
    return new_entry
