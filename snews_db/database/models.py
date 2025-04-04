from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Identity

Base = declarative_base()


class AllMessages(Base):
    __tablename__ = "all_mgs"

    id = Column(Integer, Identity(), primary_key=True)
    message_id = Column(String)
    received_time = Column(String)
    message_type = Column(String)
    message = Column(String)
    expiration = Column(String)

    def __repr__(self):
        return (
            f"<AllMessages(message_id='{self.message_id}', "
            f"received_time='{self.received_time}', "
            f"message_type='{self.message_type}')>"
        )


class SigTierArchive(Base):
    __tablename__ = "sig_tier_archive"

    id = Column(Integer, autoincrement=True, primary_key=True)
    message_id = Column(String)
    schema_version = Column(Float)
    detector_name = Column(String)
    p_vals = Column(String)
    t_bin_width_sec = Column(Float)
    is_test = Column(Integer)
    sent_time_utc = Column(String)
    machine_time_utc = Column(String)
    meta = Column(String)
    expiration = Column(String)

    def __repr__(self):
        return (
            f"<SigTierArchive(detector_name='{self.detector_name}', "
            f"schema_version='{self.schema_version}', "
            f"sent_time_utc='{self.sent_time_utc}')>"
        )


class TimeTierArchive(Base):
    __tablename__ = "time_tier_archive"

    id = Column(Integer, autoincrement=True, primary_key=True)
    message_id = Column(String)
    schema_version = Column(Float)
    detector_name = Column(String)
    p_val = Column(Float)
    t_bin_width_sec = Column(Float)
    timing_series = Column(String)
    sent_time_utc = Column(String)
    machine_time_utc = Column(String)
    meta = Column(String)
    expiration = Column(String)

    def __repr__(self):
        return (
            f"<TimeTierArchive(detector_name='{self.detector_name}', "
            f"schema_version='{self.schema_version}', "
            f"sent_time_utc='{self.sent_time_utc}')>"
        )


class CoincidenceTierArchive(Base):
    __tablename__ = "coincidence_tier_archive"

    id = Column(Integer, autoincrement=True, primary_key=True)
    message_id = Column(String)
    schema_version = Column(Float)
    detector_name = Column(String)
    p_val = Column(Float)
    neutrino_time_utc = Column(String)
    sent_time_utc = Column(String)
    machine_time_utc = Column(String)
    meta = Column(String)
    expiration = Column(String)

    def __repr__(self):
        return (
            f"<CoincidenceTierArchive(detector_name='{self.detector_name}', "
            f"schema_version='{self.schema_version}', "
            f"sent_time_utc='{self.sent_time_utc}')>"
        )


class CoincidenceTierAlerts(Base):
    __tablename__ = "coincidence_tier_alerts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    message_id = Column(String)
    alert_type = Column(String)
    server_tag = Column(String)
    false_alarm_prob = Column(String)
    detector_names = Column(String)
    sent_time_utc = Column(String)
    p_vals = Column(String)
    neutrino_times = Column(String)
    p_vals_average = Column(String)
    sub_list_number = Column(Integer)

    def __repr__(self):
        return (
            f"<CoincidenceTierAlerts(alert_type='{self.alert_type}', "
            f"server_tag='{self.server_tag}', "
            f"sent_time_utc='{self.sent_time_utc}')>"
        )


class CachedHeartbeats(Base):
    __tablename__ = "cached_heartbeats"

    id = Column(Integer, autoincrement=True, primary_key=True)
    received_time_utc = Column(DateTime)
    detector = Column(String)
    stamped_time_utc = Column(DateTime)
    latency = Column(BigInteger)
    time_after_last = Column(BigInteger)
    status = Column(String)

    def __repr__(self):
        return (
            f"<CachedHeartbeats(detector='{self.detector}', "
            f"received_time_utc='{self.received_time_utc}', "
            f"status='{self.status}')>"
        )


def create_db_engine(database_url):
    return create_engine(database_url)


def create_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
