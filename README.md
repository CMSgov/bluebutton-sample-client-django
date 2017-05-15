Blue Button Sample Client Application - Django Version
====================================================

## Which Version of Python?

This application has been tested using Python 3.5.1

## Quick Setup

    git clone https://github.com/hhsidealab/django_blubutton_client.git
    pip install -r requirements/requirements.txt
    mkdir db
    touch db/db.db
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Running the tests

To run the tests against http://oauth.npi.io/ use:

    python manage.py test --settings=hhs_oauth_client.settings.test

To run the tests against a local server instance (http://127.0.0.1:8000) use:

    python manage.py test --settings=hhs_oauth_client.settings.test_local

N.B. Remember to launch ``python manage.py load_test_data`` on the server instance
to create test users, apps and capabilities.
