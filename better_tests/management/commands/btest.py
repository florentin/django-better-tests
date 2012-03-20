"""
Original code and ideas from http://www.djangosnippets.org/snippets/1318/
Thanks crucialfelix
"""
from django.core.management.base import BaseCommand
from optparse import make_option
import sys

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )
    help = 'Runs the test suite, creating a test db IF NEEDED and NOT DESTROYING the test db afterwards.  Otherwise operates exactly as does test.'
    args = '[appname ...]'

    requires_model_validation = False

    def handle(self, *test_labels, **options):
        from django.conf import settings
        from django.test.utils import get_runner

        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive', True)

        settings.TEST_RUNNER = 'better.tests.runners.TestSuiteRunner'

        test_runner = get_runner(settings)(verbosity=verbosity, interactive=interactive)
        
        failures = test_runner.run_tests(test_labels)
        if failures:
            sys.exit(failures)
