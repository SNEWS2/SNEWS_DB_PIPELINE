import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from snews_db.database.models import Base
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseConnector:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logging.info("Database engine created.")

    def get_session(self):
        return self.SessionLocal()

    def create_all_tables(self):
        try:
            Base.metadata.create_all(bind=self.engine)
            logging.info("All tables created based on SQLAlchemy models.")
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            raise

    def execute_sql_from_file(self, file_path):
        session = self.get_session()
        try:
            with open(file_path, 'r') as f:
                sql = f.read()
                session.execute(sql)
            session.commit()
            logging.info(f"SQL executed successfully from: {file_path}")
        except FileNotFoundError:
            logging.error(f"SQL file not found: {file_path}")
            raise
        except Exception as e:
            session.rollback()
            logging.error(f"Error executing SQL from {file_path}: {e}")
            raise
        finally:
            session.close()

    def execute_query(self, query, params=None):
        session = self.get_session()
        try:
            result = session.execute(query, params)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logging.error(f"Error executing query: {e}")
            raise
        finally:
            session.close()


if __name__ == "__main__":
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    db_connector = DatabaseConnector(db_url)
    print(db_connector.engine)
    print(db_connector.SessionLocal)
    # db_connector.create_all_tables()

    # query = text("SELECT * FROM all_mgs")
    # check = db_connector.execute_query(query)
    # print(check)
    # To execute SQL from a file:
    # try:
    #     db_connector.execute_sql_from_file("snews_db/database/initialization/init_db.sql")
    # except FileNotFoundError:
    #     print("Initialization SQL file not found.")
    # except Exception as e:
    #     print(f"Error during database initialization: {e}")
    print('table(s) created')