import sys
print("wsgi.py starting...", file=sys.stderr)
# Ensure the app directory is in the Python path if needed, though usually Gunicorn handles this
# sys.path.insert(0, '/app') # Generally not required if WORKDIR is /app

# Absolute import is correct here
from create_app import create_app

print("wsgi.py: Calling create_app()...", file=sys.stderr)
app = create_app()
print("wsgi.py: create_app() returned. 'app' object created.", file=sys.stderr)

# This part is for running locally with `python wsgi.py`
if __name__ == "__main__":
    print("wsgi.py running in __main__", file=sys.stderr)
    # Use environment variable for port or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Debug should be controlled by FLASK_DEBUG env var set in Config
    app.run(host='0.0.0.0', port=port)