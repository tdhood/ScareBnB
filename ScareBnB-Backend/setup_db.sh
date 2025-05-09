#!/bin/bash
set -e

echo 'Delete and recreate scarebnb.db?'
read -p 'Return for yes or control-C to cancel > '

# Remove the existing database file if it exists
rm -f scarebnb.db

# Create and populate the main database
echo "Creating and setting up scarebnb.db..."
sqlite3 scarebnb.db < scarebnb_schema.sql
sqlite3 scarebnb.db < scarebnb_seed.sql
echo "scarebnb.db setup complete!"

echo 'Delete and recreate scarebnb_test.db?'
read -p 'Return for yes or control-C to cancel >'

# Remove the test database file if it exists
rm -f scarebnb_test.db

# Create and populate the test database
echo "Creating and setting up scarebnb_test.db..."
sqlite3 scarebnb_test.db < scarebnb_schema.sql
echo "scarebnb_test.db setup complete!"