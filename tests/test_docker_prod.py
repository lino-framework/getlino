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
    def run_docker_command(self, container, command, assertfunction=None, args=None):
        exit_code, output = container.exec_run(
            """bash -c '{}'""".format(command), user='lino')
        output = output.decode('utf-8')
        if exit_code != 0:
            msg = "%s  returned %d:\n-----\n%s\n-----" % (
                command, exit_code, output)
            self.fail(msg)
        elif assertfunction:
            getattr(self, assertfunction)(args, output)
        else:
            print(output)

    def run_production_tests(self, docker_tag):
        if docker_tag:
            if True:
                container = client.containers.run(
                    docker_tag, command="/bin/bash", user='lino', tty=True, detach=True)
                self.run_docker_command(
                    container, 'ls -l', 'assertIn', 'setup.py')
                self.run_docker_command(
                    container, 'sudo -H env PATH=$PATH pip3 install -e . ', 'assertIn', """Installing collected packages: pytz, Babel, sphinxcontrib-jsmath, sphinxcontrib-qthelp, Pygments, sphinxcontrib-serializinghtml, sphinxcontrib-devhelp, alabaster, imagesize, pyparsing, packaging, sphinxcontrib-applehelp, docutils, snowballstemmer, certifi, idna, urllib3, chardet, requests, sphinxcontrib-htmlhelp, MarkupSafe, jinja2, Sphinx, argh, future, invoke, python-dateutil, unipath, atelier, click, virtualenv, getlino""")
                # self.run_docker_command(
                #    container, 'sudo -H env PATH=$PATH getlino configure --batch --db-engine postgresql --monit ')
                self.run_docker_command(
                    container, 'sudo -H env PATH=$PATH getlino configure --batch --db-engine postgresql')
                self.run_docker_command(
                    container, "sudo -H env PATH=$PATH getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl' ")
                self.run_docker_command(
                    container, "sudo -H env PATH=$PATH getlino startsite cosi mycosi1 --batch --dev-repos 'lino cosi xl' ")
                self.run_docker_command(
                    container, 'cd /usr/local/lino/lino_local/mysite1 && ls -l')
                self.run_docker_command(
                    container, 'sudo -H env PATH=$PATH . /usr/local/lino/lino_local/mysite1/env/bin/activate && pull.sh')
                self.run_docker_command(
                    container, 'sudo -H env PATH=$PATH cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh')
                container.stop()
            if False:
                self.run_subprocess(
                    "docker run --name {} --rm -i -t -d {} bash".format(docker_tag, docker_tag).split())
                docker_run_command = """docker exec -ti {} sh -c "{}" """.format(
                    docker_tag, "{}")
                import subprocess
                subprocess.run(docker_run_command.format("bash -c ls -l"))
                self.run_subprocess(docker_run_command.split(
                ) + ['bash -c  "sudo -H pip3 install -e . "'])
                self.run_subprocess(docker_run_command.split(
                ) + ["bash -c  'sudo -H env PATH=$PATH getlino configure --batch --db-engine postgresql' "])
                self.run_subprocess(docker_run_command.split(
                ) + [""" bash -c  "sudo -H getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl'" """])
                self.run_subprocess(docker_run_command.split(
                ) + ["bash -c  'cd /usr/local/lino/lino_local/mysite1 && ls -l' "])
                self.run_subprocess(docker_run_command.split(
                ) + ["bash -c . /usr/local/lino/lino_local/mysite1/env/bin/activate && cd /usr/local/lino/lino_local/mysite1 && ./pull.sh' "])
                self.run_subprocess(docker_run_command.split(
                ) + ["bash -c 'cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh' "])

    def run_dev_tests(self, docker_tag):
        if docker_tag:
            if True:
                container = client.containers.run(
                    docker_tag, command="/bin/bash", user='lino', tty=True, detach=True)
                self.run_docker_command(
                    container, 'ls -l', 'assertIn', 'setup.py')
                self.run_docker_command(
                    container, 'pip3 install -e . ', 'assertIn', """Installing collected packages: pytz, Babel, snowballstemmer, sphinxcontrib-qthelp, sphinxcontrib-htmlhelp, pyparsing, packaging, Pygments, alabaster, urllib3, certifi, idna, chardet, requests, docutils, sphinxcontrib-applehelp, sphinxcontrib-serializinghtml, imagesize, sphinxcontrib-devhelp, MarkupSafe, jinja2, sphinxcontrib-jsmath, Sphinx, argh, future, invoke, python-dateutil, unipath, atelier, click, virtualenv, getlino""")
                self.run_docker_command(
                    container, 'getlino configure --batch --db-engine postgresql')
                self.run_docker_command(
                    container, "getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl' ")
                self.run_docker_command(
                    container, "getlino startsite cosi mycosi1 --batch --dev-repos 'lino cosi xl' ")
                self.run_docker_command(
                    container, 'cd /usr/local/lino/lino_local/mysite1 && ls -l')
                self.run_docker_command(
                    container, '. /usr/local/lino/lino_local/mysite1/env/bin/activate && pull.sh')
                self.run_docker_command(
                    container, 'cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh')

    def test_prod(self):
        self.run_production_tests("prod_debian")
        # self.run_production_tests("prod_ubuntu")

    def test_dev(self):
        pass
        # self.run_dev_tests("dev_debian")
        # self.run_dev_tests("dev_ubuntu")
