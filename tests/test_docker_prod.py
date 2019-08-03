from os.path import dirname, join
from atelier.test import TestCase
import getlino

class DockerTests(TestCase):
    def test_01(self):
        args = ['docker', 'run', 'prod', "ls -l"]
        self.run_subprocess(args)
