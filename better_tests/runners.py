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
    def __init__(self, **options):
        super(TestSuiteRunner, self).__init__(**options)
        self.options = options
        self.monkeypatch_connections()
        
    def monkeypatch_connections(self):
        """
        Monkeypatch the sqlite3 driver to use these 2 new methods
        """
    
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
                    print "sqlite test database found !"
            
            #self._create_test_db(verbosity, autoclobber)
    
            self.connection.close()
            self.connection.settings_dict["NAME"] = test_database_name
            
            # Confirm the feature set of the test database
            self.connection.features.confirm()
            
            # Get a cursor (even though we don't need one yet). This has
            # the side effect of initializing the test database.
            self.connection.cursor()

            return test_database_name
        
        def destroy_test_db(self, old_database_name, verbosity=1):
            """
            Destroy a test database, prompting the user for confirmation if the
            database already exists.
            """
            self.connection.close()
            test_database_name = self.connection.settings_dict['NAME']
            if verbosity >= 1:
                test_db_repr = ''
                if verbosity >= 2:
                    test_db_repr = " ('%s')" % test_database_name
                print "Ignore the test database for alias '%s'%s..." % (
                    self.connection.alias, test_db_repr)
                
            # Temporarily use a new connection and a copy of the settings dict.
            # This prevents the production database from being exposed to potential
            # child threads while (or after) the test database is destroyed.
            # Refs #10868 and #17786.
            settings_dict = self.connection.settings_dict.copy()
            settings_dict['NAME'] = old_database_name        
        
        def _destroy_test_db(self, test_database_name, verbosity):
            print "Keep the test database !" #%test_database_name
            self.connection.close()
        
        
        for alias in connections:
            """
            django.test.simple.DjangoTestSuiteRunner
            django.db.backends.creation
            django.db.backends.mysql.base
            """
            connection = connections[alias]
            #if connection.settings_dict.get('ENGINE', '').endswith('.sqlite3'):
            
            if not self.options['setupdbs']:
                f1 = types.MethodType(create_test_db, connection.creation, DatabaseCreation)
                connection.creation.create_test_db = f1
            
            if not self.options['teardowndbs']:
                f2 = types.MethodType(destroy_test_db, connection.creation, DatabaseCreation)
                connection.creation.destroy_test_db = f2