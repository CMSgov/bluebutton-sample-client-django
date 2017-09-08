Blue Button Sample Client Application - Django Version
======================================================

## Introduction

This client demonstrates authenticating to the Blue Buttom API and subsequent FHIR API calls.
It demonstrates the OAuth2 Server Side web application flow where a `client_secret` is used.

## Status and Contributing

This application has been tested using Python 3.5.1 and Django 1.10, but should work just fine
on Python 2.7 and 3.4. The application is in active development so check back often for updates.
Please consider improving this code with your contributions. Pull requests welcome ;)

## Basic Setup

    git clone https://github.com/hhsidealab/django_blubutton_client.git
    cd django_blubutton_client/bbc
    pip install -r requirements/requirements.txt
    mkdir db
    python manage.py migrate
    python manage.py runserver

## Set and Adjust your Settings.

You must register an client application and set settings values for:

  * `SOCIAL_AUTH_OAUTH2IO_KEY`
  * `SOCIAL_AUTH_OAUTH2IO_SECRET`

You can override the host with which your are communicating by adjusting these settings:

  *  `OAUTH2IO_HOST`   - the default is `https://dev.bluebutton.cms.fhirservice.net`
  *  `EXTERNAL_AUTH_NAME` - the default is `CMS`.

If you change the `OAUTH2IO_HOST` to something non https (for testing), then you need to
tell the oauthlib to operate in an insecure mode like so.

    import os 
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

## Running the Tests

To run the tests against https://dev.bluebutton.cms.fhirservice.net use:

    python manage.py test --settings=bbc.settings.test

To run the tests against a local OAuth2/FHIR server instance (http://localhost:8000) use:

    python manage.py test --settings=bbc.settings.test_local
