# Procfile for deployment
# Choose one of the following based on your deployment needs:

# For running both bot and web app together
web: gunicorn -b 0.0.0.0:$PORT app:app --workers 1 --threads 2 --timeout 120

# Alternative: For running bot and web app separately
# web: gunicorn -b 0.0.0.0:$PORT app:app
# worker: python bot.py