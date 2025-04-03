from sqlalchemy.orm import Session
from .database.models import (
    AllMessages,
    SigTierArchive,
    TimeTierArchive,
    CoincidenceTierArchive,
    CoincidenceTierAlerts,
    CachedHeartbeats,
)


def add_all_message(
    session: Session,
    message_id: str,
    received_time: str,
    message_type: str,
    message: str,
    expiration: str,
):
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


def add_sig_tier_archive(
    session: Session,
    message_id: str,
    schema_version: float,
    detector_name: str,
    p_vals: str,
    t_bin_width_sec: float,
    is_test: int,
    sent_time_utc: str,
    machine_time_utc: str,
    meta: str,
    expiration: str,
):
    new_sig_tier = SigTierArchive(
        message_id=message_id,
        schema_version=schema_version,
        detector_name=detector_name,
        p_vals=p_vals,
        t_bin_width_sec=t_bin_width_sec,
        is_test=is_test,
        sent_time_utc=sent_time_utc,
        machine_time_utc=machine_time_utc,
        meta=meta,
        expiration=expiration,
    )
    session.add(new_sig_tier)
    session.commit()
    return new_sig_tier


def add_time_tier_archive(
    session: Session,
    message_id: str,
    schema_version: float,
    detector_name: str,
    p_val: float,
    t_bin_width_sec: float,
    timing_series: str,
    sent_time_utc: str,
    machine_time_utc: str,
    meta: str,
    expiration: str,
):
    new_time_tier = TimeTierArchive(
        message_id=message_id,
        schema_version=schema_version,
        detector_name=detector_name,
        p_val=p_val,
        t_bin_width_sec=t_bin_width_sec,
        timing_series=timing_series,
        sent_time_utc=sent_time_utc,
        machine_time_utc=machine_time_utc,
        meta=meta,
        expiration=expiration,
    )
    session.add(new_time_tier)
    session.commit()
    return new_time_tier


def add_coincidence_tier_archive(
    session: Session,
    message_id: str,
    schema_version: float,
    detector_name: str,
    p_val: float,
    t_bin_width_sec: float,
    timing_series: str,
    sent_time_utc: str,
    machine_time_utc: str,
    meta: str,
    expiration: str,
):

    new_coincidence_tier = CoincidenceTierArchive(
        message_id=message_id,
        schema_version=schema_version,
        detector_name=detector_name,
        p_val=p_val,
        t_bin_width_sec=t_bin_width_sec,
        timing_series=timing_series,
        sent_time_utc=sent_time_utc,
        machine_time_utc=machine_time_utc,
        meta=meta,
        expiration=expiration,
    )
    session.add(new_coincidence_tier)
    session.commit()
    return new_coincidence_tier


def add_coincidence_tier_alerts(
    session: Session,
    message_id: str,
    schema_version: float,
    detector_name: str,
    p_val: float,
    sent_time_utc: str,
    machine_time_utc: str,
    meta: str,
    expiration: str,
):
    new_coincidence_tier_alert = CoincidenceTierAlerts(
        message_id=message_id,
        schema_version=schema_version,
        detector_name=detector_name,
        p_val=p_val,
        sent_time_utc=sent_time_utc,
        machine_time_utc=machine_time_utc,
        meta=meta,
        expiration=expiration,
    )
    session.add(new_coincidence_tier_alert)
    session.commit()
    return new_coincidence_tier_alert


def add_cached_heartbeats(
    session: Session, detector_name: str, sent_time_utc: str, machine_time_utc: str, meta: str
):
    new_cached_heartbeat = CachedHeartbeats(
        detector_name=detector_name,
        sent_time_utc=sent_time_utc,
        machine_time_utc=machine_time_utc,
        meta=meta,
    )
    session.add(new_cached_heartbeat)
    session.commit()
    return new_cached_heartbeat
