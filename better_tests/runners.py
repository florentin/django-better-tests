__author__ = 'florentin.sardan'

import os, sys
from django.db.backends.sqlite3.creation import DatabaseCreation
from django.test.simple import DjangoTestSuiteRunner
from django.db import connections
import types

class TestSuiteRunner(DjangoTestSuiteRunner):
    """
    If the test database doesn't exist, behave like the normal test runner except 
    for the fact i'm not deleting it after the test is done
    If the test database exists, leave it alone and print some warning messages.
    """
    def __init__(self, verbosity=1, interactive=True, failfast=True, **kwargs):
        super(TestSuiteRunner, self).__init__(verbosity, interactive, failfast, **kwargs)
        self.monkeypatch_connections()
    
    def monkeypatch_connections(self):
        """
        Monkeypatch the sqlite3 driver to use these 2 new methods
        """
           
        def _destroy_test_db(self, test_database_name, verbosity):
            print "Keep the test database !" #%test_database_name
            self.connection.close()
        
        def create_test_db(self, verbosity=1, autoclobber=False):
            """
            Creates a test database, prompting the user for confirmation if the
            database already exists. Returns the name of the test database created.
            """
            # Don't import django.core.management if it isn't needed.
            test_database_name = self._get_test_db_name()
            
            if self.connection.settings_dict.get('ENGINE', '').endswith('.sqlite3')\
                and test_database_name != ':memory:':
                if os.access(test_database_name, os.F_OK):
                    print "Found a sqlite test database !" #%test_database_name
            
            #self._create_test_db(verbosity, autoclobber)
    
            self.connection.close()
            self.connection.settings_dict["NAME"] = test_database_name
            
            # Confirm the feature set of the test database
            self.connection.features.confirm()
            
            # Get a cursor (even though we don't need one yet). This has
            # the side effect of initializing the test database.
            cursor = self.connection.cursor()

            return test_database_name
        
        for alias in connections:
            connection = connections[alias]
            #if connection.settings_dict.get('ENGINE', '').endswith('.sqlite3'):
            f1 = types.MethodType(create_test_db, connection.creation, DatabaseCreation)
            connection.creation.create_test_db = f1
            
            f2 = types.MethodType(_destroy_test_db, connection.creation, DatabaseCreation)
            connection.creation._destroy_test_db = f2
