#!/usr/bin/env python
import os
import sys
import django

from django.conf import settings
from django.test.utils import get_runner


if __name__ == '__main__':
    #sys.path.append(os.path.realpath(__file__))
    retval = os.getcwd()
    path = retval + "/bbc"
    print("PATH", path)
    os.chdir(path)
    print(path)
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bbc.settings.local'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(None)
    sys.exit(bool(failures))
