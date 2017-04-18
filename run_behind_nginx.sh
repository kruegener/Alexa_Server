python manage.py runworker --threads 4 &
daphne -b 127.0.0.1 -p 8000 AlexaHandler.asgi:channel_layer &
