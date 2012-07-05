# Django Better Tests

A testing app for Django.

## Installation

* add "better.tests" to INSTALLED_APPS
* add the "TEST_NAME" to the DATABASES["default"] dictionary

## Usage
$ python manage.py btest

## How to keep the test database
* create a file tests/utils.py with the following class
class TestMixin(object):
    fixtures = []
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

* use this mixin in your TestCase definition

