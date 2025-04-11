import os
import sys

# Dodaj katalog główny projektu do sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importuj bazę modeli (Base) oraz modele
from app.core.database import Base
from app.models.users import *
from app.models.animals import *
from app.models.appointments import *

config = context.config

# Interpretacja konfiguracji z pliku alembic.ini
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
