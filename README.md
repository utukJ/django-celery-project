# django-celery-project
REST API written in Django exposing endpoints for performing CRUD on conversations and chats within conversations. Celery is used to schedule date for sending chat!

## Setup
- clone the repo
- cd into the cloned repo directory and run <pipenv install -r requirements.txt>
- run the celery instance using <celery -A config worker --loglevel=INFO --pool=solo>
- run the project using <py manage.py runserver>

## Testing
