import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

config = context.config
fileConfig(config.config_file_name)

def get_url() -> str:
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    name = os.environ["DB_NAME"]
    user = os.environ["DB_USER"]
    pwd  = os.environ["DB_PASS"]
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}"

def run_migrations_online() -> None:
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
