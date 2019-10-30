from os.path import dirname, join
from atelier.test import TestCase
import getlino

if False:  # no sure whether we will need it again
  class DockerTests(TestCase):
    def test_prod_debian(self):
        args = ['docker', 'run', 'prod_debian', "ls -l"]
        self.run_subprocess(args)

    def test_prod_ubuntu(self):
        args = ['docker', 'run', 'prod_ubuntu', "ls -l"]
        self.run_subprocess(args)
