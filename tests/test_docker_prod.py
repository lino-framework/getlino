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
    def test_prod_debian(self):
        self.run_subprocess(
            docker_debian_command + ['cd /usr/local/lino/lino_local/mysite1 && ls -l'])
        self.run_subprocess(
            docker_debian_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && pull.sh '])
        self.run_subprocess(
            docker_debian_command + ['cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh '])
        self.run_subprocess(
            docker_debian_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && exec python manage.py runserver '])
        self.run_subprocess(
            docker_debian_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && exec python manage.py runserver'])

    def test_prod_ubuntu(self):
        self.run_subprocess(
            docker_ubuntu_command + ['cd /usr/local/lino/lino_local/mysite1 && ls -l'])
        self.run_subprocess(
            docker_ubuntu_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && pull.sh '])
        self.run_subprocess(
            docker_ubuntu_command + ['cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh '])
        self.run_subprocess(
            docker_ubuntu_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && exec python manage.py runserver '])
        self.run_subprocess(
            docker_ubuntu_command + ['. /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && exec python manage.py runserver'])
