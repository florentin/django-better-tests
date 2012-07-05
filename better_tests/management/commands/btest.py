import sys
from optparse import make_option, OptionParser
from django.conf import settings

try:
    from south.management.commands import test
except ImportError:
    from django.core.management.commands import test

class Command(test.Command):
    option_list = test.Command.option_list + (
        make_option('--teardowndbs',
            action='store_true', dest='teardowndbs', default=False,
            help='Tells Django weather to teardown the databases.'),
        make_option('--setupdbs',
            action='store_true', dest='setupdbs', default=False,
            help='Tells Django weather to setup the databases.') 
    )
    
    # TODO: remove the test_runner option
    
    def handle(self, *test_labels, **options):
        if 'test_runner' in options:
            sys.exit('You are not allowed to use the "test_runner" option with the "btest" command.')
        options['testrunner'] = 'better_tests.runners.TestSuiteRunner'
        super(Command, self).handle(*test_labels, **options)

