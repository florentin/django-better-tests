# Django Better Tests

A testing app for Django.

## Installation

* add "better.tests" to INSTALLED_APPS
* add the "TEST_NAME" to the DATABASES["default"] dictionary

## Usage
* this will create and destroy the test database
$ python manage.py btest api.ApiTests.test_create --setupdbs --teardowndbs

* this will ignore the creation/deletion process of the test database
$ python manage.py btest api.ApiTests.test_create

## How to keep the test database
* create a file tests/utils.py with the following class
class TestMixin(object):
    fixtures = []
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

* use this mixin in your TestCase definition

