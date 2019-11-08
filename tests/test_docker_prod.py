from os.path import dirname, join
from atelier.test import TestCase
import docker
import getlino

client = docker.from_env()

"""
>>> from atelier.sheller import Sheller
>>> shell = Sheller('docs/dev/hello')
>>> shell("whoami")
linox
>>> shell("sudo -H env PATH=$PATH getlino configure --batch")
... #doctest: +ELLIPSIS +REPORT_UDIFF
"""


class DockerTests(TestCase):
    def run_commands_for(self, docker_tag):
        if docker_tag:
            client.containers.run(docker_tag, "sudo -H pip3 install -e .")
            client.containers.run(docker_tag,"sudo -H getlino configure --batch --db-engine postgresql")
            client.containers.run(docker_tag,"sudo -H getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl'")
            client.containers.run(docker_tag,["cd /usr/local/lino/lino_local/mysite1","ls -l"])
            client.containers.run(docker_tag,[". /usr/local/lino/lino_local/mysite1/env/bin/activate","pull.sh"])
            client.containers.run(docker_tag,["cd /usr/local/lino/lino_local/mysite1","./make_snapshot.sh"])
            client.containers.run(docker_tag,[". /usr/local/lino/lino_local/mysite1/env/bin/activate","cd /usr/local/lino/lino_local/mysite1" , "exec python manage.py runserver"])

    def test_prod_debian(self):
        self.run_commands_for("prod_debian")

    def test_prod_ubuntu(self):
        self.run_commands_for("prod_ubuntu")
