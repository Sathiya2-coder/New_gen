#!/usr/bin/env python
"""
Run direct ALTER statements against the database without creating the Flask app
This avoids app startup logic (like creating admin user) that can fail before schema changes.

Usage:
    python run_alters.py

"""
from sqlalchemy import create_engine, text
import sys

try:
    # Import Config safely (reads .env) to get DATABASE_URL
    from config import Config
    db_url = Config.SQLALCHEMY_DATABASE_URI
except Exception:
    print("Could not import Config; ensure config.py is present and readable.")
    sys.exit(1)

ALTER_STATEMENTS = [
    # Expand password column to accommodate longer hashes
    "ALTER TABLE users ALTER COLUMN password TYPE VARCHAR(512);",

    # Add theme_settings timestamp columns if missing
    "ALTER TABLE theme_settings ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE theme_settings ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",

    # Ensure teams/persons/contact_messages have timestamps too
    "ALTER TABLE teams ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE teams ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE persons ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE persons ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    # Add users.created_at and last_login if missing
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP WITH TIME ZONE;",
]

print("Connecting to DB:", db_url)
engine = create_engine(db_url)

with engine.begin() as conn:
    for stmt in ALTER_STATEMENTS:
        try:
            print("Running:", stmt)
            conn.execute(text(stmt))
            print("OK")
        except Exception as e:
            print("Failed:", stmt)
            print("  ", e)

print("Done. If ALTERs succeeded, restart the app or run seed_database.py.")
