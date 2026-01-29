from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.core.database import Base
from app.models import resume, job, evaluation  # import model để load metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


config.set_main_option(
    "sqlalchemy.url",
    settings.SQLALCHEMY_DATABASE_URI
)

target_metadata = Base.metadata


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True  
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()