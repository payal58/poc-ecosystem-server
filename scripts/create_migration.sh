#!/bin/bash
# Script to create initial migration
# Run: bash scripts/create_migration.sh

echo "Creating initial migration..."
alembic revision --autogenerate -m "Initial migration"
echo "✅ Migration created!"
echo "Run 'alembic upgrade head' to apply migrations"




