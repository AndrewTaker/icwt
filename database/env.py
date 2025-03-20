import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, text

from app.config import Config as app_config

# Database Connection URL
DSN: str = "postgresql+psycopg2://{user}:{password}@{host}/{dbname}".format(
    **app_config.PSQL_CONFIG
)

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def run_migrations_online() -> None:
    connectable = create_engine(DSN)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        migrations_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "migrations")
        )
        done_dicrectory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "migrations", "done")
        )

        with connection.begin():
            for file in sorted(os.listdir(migrations_directory)):
                if file.endswith(".sql") and file not in os.listdir(done_dicrectory):
                    sql_file_path = os.path.join(migrations_directory, file)
                    with open(sql_file_path, "r") as f:
                        sql_script = f.read()
                        connection.exec_driver_sql(sql_script)
                        print(f"migrate -> {sql_file_path}")

            context.get_bind().commit()


run_migrations_online()
