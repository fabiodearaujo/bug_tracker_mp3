python -m pip install --upgrade pip
pip inatall -r requirements.txt
gunicorn --bind 0.0.0.0:5000 wsgi:app