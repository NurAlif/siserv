#!/bin/bash

# Database to be dropped
DB_NAME="lingojourn_db"

# User with privileges to drop databases (e.g., the default 'postgres' superuser)
ADMIN_USER="postgres"

# The database to connect to for running the drop command (cannot be the one you're dropping)
MAINTENANCE_DB="postgres"

echo "Attempting to drop database '$DB_NAME'..."

# Execute the DROP DATABASE command
psql -U "$ADMIN_USER" -d "$MAINTENANCE_DB" -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "Database '$DB_NAME' has been dropped (if it existed)."

sudo -u postgres dropdb --if-exists lingojourn_db

sudo -u postgres createdb -O oftg lingojourn_db

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE lingojourn_db TO oftg;"

UPDATE users SET role = 'teacher' WHERE username = 'prof_davis';

sudo psql -d lingojourn_db -U oftg -h localhost

UPDATE users SET is_admin = TRUE WHERE username = 'a';

sudo psql -U oftg -d lingojourn_db -f students.sql -h localhost