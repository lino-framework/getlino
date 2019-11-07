from os.path import dirname, join
from atelier.test import TestCase
import getlino

docker_debian_command = 'docker run prod_debian /bin/bash -c '.split()
docker_ubuntu_command = 'docker run prod_ubuntu /bin/bash -c '.split()

"""
>>> from atelier.sheller import Sheller
>>> shell = Sheller('docs/dev/hello')
>>> shell("whoami")
linox
>>> shell("sudo -H env PATH=$PATH getlino configure --batch")
... #doctest: +ELLIPSIS +REPORT_UDIFF

"""


class DockerTests(TestCase):
    def run_commands_for(self, docker_command):
        if docker_command:
            self.run_subprocess(
                docker_command + ['sudo -H getlino configure --batch --db-engine postgresql'])
            self.run_subprocess(
                docker_command + [""" "sudo -H getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl'" """])
            self.run_subprocess(
                docker_command + ['cd /usr/local/lino/lino_local/mysite1 && ls -l'])
            self.run_subprocess(
                docker_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && pull.sh '])
            self.run_subprocess(
                docker_command + ['cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh '])
            self.run_subprocess(
                docker_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && exec python manage.py runserver '])
            self.run_subprocess(
                docker_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && exec python manage.py runserver'])
        else:
            print("You need to set the docker command")

    def test_prod_debian(self):
        self.run_commands_for(docker_debian_command)

    def test_prod_ubuntu(self):
        self.run_commands_for(docker_ubuntu_command)
