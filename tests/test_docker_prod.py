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
            if True:
                container  = client.containers.run(docker_tag,command="/bin/bash", user='lino',tty=True,detach=True)
                container.logs()
                print(container)
                print(container.exec_run( "bash -c 'ls -l'",user='lino'))
                print(container.exec_run( "bash -c 'sudo -H pip3 install -e . '",user='lino'))
                print(container.exec_run( "bash -c 'sudo -H env PATH=$PATH getlino configure --batch --db-engine postgresql '",user='lino'))
                print(container.exec_run( """ bash -c 'sudo -H getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl' '"""))
                print(container.exec_run( "bash -c  'cd /usr/local/lino/lino_local/mysite1 && ls -l'"))
                print(container.exec_run( "bash -c  '. /usr/local/lino/lino_local/mysite1/env/bin/activate && ./pull.sh'"))
                print(container.exec_run( "bash -c  'cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh' "))
            if False:
                self.run_subprocess("docker run --name {} --rm -i -t -d {} bash".format(docker_tag,docker_tag).split())
                docker_run_command = """docker exec -ti {} sh -c "{}" """.format(docker_tag,"{}")
                import subprocess
                subprocess.run(docker_run_command.format("ls -l"))
                self.run_subprocess(docker_run_command.split() + ['"sudo -H pip3 install -e . "'])
                self.run_subprocess(docker_run_command.split() + ["sudo -H env PATH=$PATH getlino configure --batch --db-engine postgresql"])
                self.run_subprocess(docker_run_command.split() + [" sudo -H getlino startsite noi mysite1 --batch --dev-repos 'lino noi xl'"])
                self.run_subprocess(docker_run_command.split() + [" cd /usr/local/lino/lino_local/mysite1 && ls -l"])
                self.run_subprocess(docker_run_command.split() + [" . /usr/local/lino/lino_local/mysite1/env/bin/activate && ./pull.sh"])
                self.run_subprocess(docker_run_command.split() + [" cd /usr/local/lino/lino_local/mysite1 && ./make_snapshot.sh"])


    def test_prod_debian(self):
        self.run_commands_for("getlino")

    def test_prod_ubuntu(self):
        return
        self.run_commands_for("prod_ubuntu")
