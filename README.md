Blue Button Sample Client Application - Django Version
======================================================

## Introduction

This client demonstrates authenticating to the Blue Buttom API and subsequent FHIR API calls.
It demonstrates the OAuth2 Server Side web application flow where a `client_secret` is used.

## Status and Contributing

The application is in active development so check back often for updates.
Please consider improving this code with your contributions. Pull requests welcome ;)

## Basic Setup

    git clone https://github.com/HHSIDEAlab/django_bluebutton_client.git
    cd django_blubutton_client/bbc

While not required, using `virtualenv` is a good idea. 
The following commands work for Python 3+. Please search `virtualenv` 
to fine eqivilent commands to install and setup `virtualenv` for Python 2.7.


    python -m venv venv
    source venv/bin/activate

The following command assumes a `virtualenv` was created and activated. 
If you aren't using `virtualenv`, then you may need to put `sudo` in 
front of the following `pip` command.

    pip install -r requirements/requirements.in
    cp bbc/settings/local_sample.py bbc/settings/local.py
    python manage.py migrate --settings bbc.settings.local

### Configuring Your Development Application

By default, your application will be set up to use the public OAuth service
at https://sandbox.bluebutton.cms.gov/. In order to use this version of
the service, you'll need to request an account on that site. So go to
https://sandbox.bluebutton.cms.gov and choose "+Signup" in the top navigation bar.
Fill out the form, setting user type to "Developer".

Once you have your developer account created and you've verified your email address,
you'll need to set up an application. Log in to your new account, and select
"Applications" -> "Applications You Created" -> "Register New Application". From
here, you can fill out the form with the following options:

    Scope: [you likely want to select all available]
    Name: [your choice]
    Client type: Confidential
    Authorization grant type: Authorization Code
    Redirect uris: http://localhost:8000/social-auth/complete/oauth2io/

Once you submit the form, you should receive an application key and secret that
can be be added to the bbc/settings/local.py file you created above, overwriting
the values for:

  * `SOCIAL_AUTH_OAUTH2IO_KEY`
  * `SOCIAL_AUTH_OAUTH2IO_SECRET`

Client ID is entered in the "SOCIAL_AUTH_OAUTH2IO_KEY" variable.
Client Secret is entered in the "SOCIAL_AUTH_OAUTH2IO_SECRET" variable.

### Final Steps

Finally, you're ready to execute

    python manage.py runserver --settings bbc.settings.local  --insecure

The --insecure option ensures that static files are loaded when running locally.

And from here, you can navigate to http://localhost:8000 and test your application.

## Other Settings

  *  `OAUTH2IO_HOST`   - the default is `https://sandbox.bluebutton.cms.gov `
  *  `EXTERNAL_AUTH_NAME` - the default is `CMS`.

If you change the `OAUTH2IO_HOST` to something non https (for testing), then you need to
tell the oauthlib to operate in an insecure mode like so.

    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

## Running the Tests

To run the tests against https://sandbox.bluebutton.cms.gov use:

    python manage.py test --settings=bbc.settings.test

To run the tests against a local OAuth2/FHIR server instance (http://localhost:8000) use:

    python manage.py test --settings=bbc.settings.test_local
