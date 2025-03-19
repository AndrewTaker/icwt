import os

PSQL_CONFIG = {
    'dbname': os.getenv("PSQL_DB_NAME", "dev"),
    'user': os.getenv("PSQL_USER", "dev"),
    'password': os.getenv("PSQL_PASSWORD", "dev"),
    'host': os.getenv("PSQL_HOST", "localhost"),
    'port': os.getenv("PSQL_PORT", 5432),
}


class Config:
    DEBUG = True
    SECRET_KEY = 'test'
    PSQL_CONFIG = PSQL_CONFIG
    DATABASE_URL = "dbname={dbname} user={user} password={password} host={host} port={port}".format(
        **PSQL_CONFIG
    )
