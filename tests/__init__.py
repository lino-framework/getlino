from getlino import SETUP_INFO

from atelier.test import TestCase


class PackagesTests(TestCase):
    def test_01(self):
        self.run_packages_test(SETUP_INFO['packages'])

    def test_developer_mode(self):
        self.run_subprocess(['getlino', 'configure'])
        self.run_subprocess(['getlino', 'startsite', 'noi', 'first'])
