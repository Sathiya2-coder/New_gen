#!/usr/bin/env python
"""
Script to alter existing PostgreSQL tables to add missing columns used by the models.
Run with the virtualenv active:

    python update_schema.py

This will run a set of safe `ALTER TABLE ... ADD COLUMN IF NOT EXISTS ...` statements.
"""
from app import create_app
from models.database import db
from sqlalchemy import text

ALTER_STATEMENTS = [
    # Theme settings timestamps
    "ALTER TABLE theme_settings ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE theme_settings ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",

    # Teams timestamps
    "ALTER TABLE teams ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE teams ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",

    # Persons timestamps
    "ALTER TABLE persons ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE persons ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",

    # Contact messages timestamps
    "ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT now();",

    # Users timestamps (if your users table doesn't have created_at/last_login)
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT now();",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP WITH TIME ZONE;",
]


def run():
    app = create_app()
    with app.app_context():
        print("Connecting to database:", db.engine.url)
        for stmt in ALTER_STATEMENTS:
            try:
                db.session.execute(text(stmt))
                db.session.commit()
                print("OK:", stmt)
            except Exception as e:
                # Rollback and continue to next statement
                db.session.rollback()
                print("Failed:", stmt)
                print("  ", e)

        print("Schema update complete.")


if __name__ == '__main__':
    run()
