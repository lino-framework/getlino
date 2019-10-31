from os.path import dirname, join
from atelier.test import TestCase
import getlino

class DockerTests(TestCase):
  def test_prod_debian(self):
      self.run_subprocess('docker build -t prod_debian -f docker/prod/Dockerfile .'.split())
      self.run_subprocess(['docker', 'run', 'prod_debian', "ls -l"])

  def test_prod_ubuntu(self):
      self.run_subprocess('docker build -t prod_debian -f docker/prod/Dockerfile_ubuntu .'.split())
      self.run_subprocess('docker run prod_ubuntu ls -l'.split())
