from alembic.config import Config
from alembic import command
from sqlalchemy import inspect
from app import db_session


def check_table_exists(table_name):
    inspector = inspect(db_session.bind)
    return table_name in inspector.get_table_names()


def run_migrations():
    if not check_table_exists("chat_history"):
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")  # Run migrations only if the table does not exist
    else:
        print("Table 'chat_history' already exists. Skipping migrations.")
