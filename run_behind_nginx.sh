sudo python manage.py runworker & sudo daphne -b 127.0.0.1 -p 8000 AlexaHandler.asgi:channel_layer