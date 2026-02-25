#!/bin/bash
set -e

echo "Starting Camping ACA Luján application..."

# Wait for database to be ready
echo "Waiting for database..."
python << END
import sys
import time
import psycopg2
import os
import socket

db_name = os.environ.get('DB_NAME', 'camping_aca_eb')
db_user = os.environ.get('DB_USER', 'devlink')
db_password = os.environ.get('DB_PASSWORD', '@Inf124578..')
maint_db = os.environ.get('DB_MAINTENANCE_DB', 'postgres')

# Candidate hosts: primary (local) first, then fallback (external)
candidates = [
    (os.environ.get('DB_HOST', 'devlink_db'),     os.environ.get('DB_PORT', '5455')),
    (os.environ.get('DB_FALLBACK_HOST', '200.58.107.187'), os.environ.get('DB_FALLBACK_PORT', '5456')),
]

def try_connect(host, port, database, timeout=5):
    return psycopg2.connect(
        host=host, port=port, database=database,
        user=db_user, password=db_password,
        connect_timeout=timeout
    )

# Resolve which host is reachable
resolved_host = None
resolved_port = None

for host, port in candidates:
    try:
        conn = try_connect(host, port, maint_db)
        conn.close()
        resolved_host = host
        resolved_port = port
        print(f"Resolved DB host: {host}:{port}")
        break
    except Exception as e:
        print(f"Cannot reach {host}:{port} -> {str(e).strip()}")

if resolved_host is None:
    print("ERROR: No database host is reachable.")
    sys.exit(1)

# Write resolved connection for bash to export
with open('/tmp/db_resolved.env', 'w') as f:
    f.write(f"DB_HOST={resolved_host}\n")
    f.write(f"DB_PORT={resolved_port}\n")

# Ensure target database exists (idempotent)
try:
    maint_conn = try_connect(resolved_host, resolved_port, maint_db)
    maint_conn.autocommit = True
    with maint_conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone() is not None
        if not exists:
            cur.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created")
        else:
            print(f"Database '{db_name}' already exists")
    maint_conn.close()
except Exception as e:
    print("Warning: could not ensure database exists:")
    print(str(e).strip())

# Wait until the target database is ready
max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = try_connect(resolved_host, resolved_port, db_name)
        conn.close()
        print("Database is ready!")
        sys.exit(0)
    except psycopg2.OperationalError as e:
        retry_count += 1
        print(f"Database not ready yet... ({retry_count}/{max_retries})")
        print(str(e).strip())
        time.sleep(3)

print("Could not connect to database after multiple retries")
sys.exit(1)
END

# Export the resolved DB host/port so Django uses the correct connection
if [ -f /tmp/db_resolved.env ]; then
    set -a
    source /tmp/db_resolved.env
    set +a
    echo "Using DB_HOST=${DB_HOST} DB_PORT=${DB_PORT}"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput
python manage.py migrate --noinput --run-syncdb

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python << END
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@campingacalujan.com',
        password='admin123'  # Change this in production!
    )
    print("Superuser 'admin' created with password 'admin123'")
    print("IMPORTANT: Change this password immediately in production!")
else:
    print("Superuser already exists")
END

# Create site configuration if it doesn't exist
echo "Setting up site configuration..."
python manage.py shell << END
from apps.landing.models import SiteConfiguration
config = SiteConfiguration.get_config()
print(f"Site configuration ready: {config.site_name}")
END

# Load initial data if needed
echo "Loading initial data..."
python manage.py load_initial_data || echo "Initial data already loaded or error occurred"

echo "Application is ready!"

# Execute the main command
exec "$@"
