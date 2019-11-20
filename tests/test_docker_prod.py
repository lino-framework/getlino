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
    def run_docker_command(self, container, command):
        exit_code, output = container.exec_run(
            """bash -c '{}'""".format(command), user='lino')
        output = output.decode('utf-8')
        if exit_code != 0:
            msg = "%s  returned %d:\n-----\n%s\n-----" % (
                command, exit_code, output)
            self.fail(msg)
        else:
            return output

    def setup_production_server(self, docker_tag):
        """

        Test the instrucations written on
        https://www.lino-framework.org/admin/install.html

        """
        container = client.containers.run(
            docker_tag, command="/bin/bash", user='lino', tty=True, detach=True)
        res = self.run_docker_command(
            container, 'ls -l')
        self.assertIn('setup.py',res)
        res = self.run_docker_command(
            container, 'sudo -H env PATH=$PATH pip3 install -e . ')
        self.assertIn("Installing collected packages:",res)
        res = self.run_docker_command(
            container, 'sudo -H env PATH=$PATH getlino configure --batch --db-engine postgresql')
        self.assertIn('getlino configure completed',res)
        res = self.run_docker_command(
            container, "sudo -H env PATH=$PATH getlino startsite noi noi1 --batch --dev-repos 'lino noi xl' ")
        self.assertIn('The new site noi1 has been created.',res)
        res = self.run_docker_command(
            container, "sudo -H env PATH=$PATH getlino startsite cosi cosi1 --batch --dev-repos 'lino cosi xl' ")
        self.assertIn('The new site cosi1 has been created.',res)
        res = self.run_docker_command(
            container, '. /etc/getlino/lino_bash_aliases')
        res = self.run_docker_command(
            container, 'go noi1 && ls -l')
        print(res)
        res = self.run_docker_command(
            container, 'a && pull.sh')
        print(res)
        res = self.run_docker_command(
            container, './make_snapshot.sh')
        print(res)
        container.stop()

    def setup_developer_env(self, docker_tag):
        """

        Test the instrucations written on
        https://www.lino-framework.org/dev/install/index.html

        """
        container = client.containers.run(
            docker_tag, command="/bin/bash", user='lino', tty=True, detach=True)
        res = self.run_docker_command(
            container, 'ls -l')
        self.assertIn('setup.py',res)
        res = self.run_docker_command(
            container, 'sudo -H env PATH=$PATH pip3 install -e . ')
        self.assertIn("Installing collected packages:",res)
        res = self.run_docker_command(
            container, 'getlino configure --batch --db-engine postgresql')
        self.assertIn('getlino configure completed',res)
        res = self.run_docker_command(
            container, "getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl' ")
        self.assertIn('The new site mysite1 has been created.',res)
        res = self.run_docker_command(
            container, "getlino startsite cosi mycosi1 --batch --dev-repos 'lino cosi xl' ")
        self.assertIn('The new site mycosi1 has been created.',res)
        res = self.run_docker_command(
            container, 'cd /usr/local/lino/lino_local/mysite1 && ls -l')
        print(res)
        res = self.run_docker_command(
            container, 'cd /usr/local/lino/lino_local/mysite1 && a && pull.sh')
        print(res)
        res = self.run_docker_command(
            container, 'cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh')
        print(res)

    def test_prod_debian(self):
        self.setup_production_server("getlino_debian")

    def test_prod_ubuntu(self):
        self.setup_production_server("getlino_ubuntu")

    def test_dev_debian(self):
        self.setup_developer_env("getlino_debian")

    def test_dev_ubuntu(self):
        self.setup_developer_env("getlino_ubuntu")
