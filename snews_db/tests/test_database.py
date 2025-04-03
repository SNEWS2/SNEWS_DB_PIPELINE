import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import Base, AllMessages
from snews_db.db_operations import add_all_message

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
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()

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
    pass

