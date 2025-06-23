# start.sh
#!/bin/bash
python -c 'from app import init_db; init_db()' # Ensure DB is initialized on startup
gunicorn --bind 0.0.0.0:$PORT app:app