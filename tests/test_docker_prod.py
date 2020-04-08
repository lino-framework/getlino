# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from os.path import dirname, join
import time
from atelier.test import TestCase
import docker
import getlino

client = docker.from_env()


class DockerTestMixin:
    docker_tag = None

    def setUp(self):
        if self.docker_tag is None:
            return
        self.container = client.containers.run(
            self.docker_tag, command="/bin/bash", user='lino', tty=True, detach=True)

    def tearDown(self):
        if self.docker_tag is None:
            return
        self.container.stop()

    def run_docker_command(self, command):
        # exit_code, output = container.exec_run(command, user='lino')
        print("===== run in {} : {} =====".format(self.container, command))
        assert not "'" in command
        exit_code, output = self.container.exec_run(
            """bash -c '{}'""".format(command), user='lino')
        output = output.decode('utf-8')
        if exit_code != 0:
            msg = "%s  returned %d:\n-----\n%s\n-----" % (
                command, exit_code, output)
            self.fail(msg)
        else:
            return output

    def do_test_production_server(self, application):
        """

        Test the instrucations written on
        https://www.lino-framework.org/admin/install.html

        """
        # load bash aliases
        # res = self.run_docker_command(
        #    container, 'source /etc/getlino/lino_bash_aliases')
        site_name = "{}1".format(application)
        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        # create and activate a virtualenv
        self.run_docker_command(
            'sudo mkdir -p /usr/local/lino/shared/env')
        self.run_docker_command(
            'cd /usr/local/lino/shared/env && sudo chown root:www-data .  && sudo chmod g+ws . && virtualenv -p python3 master')
        res = self.run_docker_command(
            'source /usr/local/lino/shared/env/master/bin/activate && sudo  pip3 install -e .')
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        # print(self.run_docker_command(container, "sudo cat /etc/getlino/lino_bash_aliases"))
        res = self.run_docker_command(
            '. /usr/local/lino/shared/env/master/bin/activate &&  sudo getlino configure --batch --db-engine postgresql --monit')
        self.assertIn('getlino configure completed', res)
        res = self.run_docker_command(
            '. /usr/local/lino/shared/env/master/bin/activate && sudo getlino startsite {} {} --batch --dev-repos "lino xl noi"'.format(application, site_name))
        self.assertIn('The new site noi1 has been created.', res)
        self.assertIn(
            'The new site {} has been created.'.format(site_name), res)
        res = self.run_docker_command(
            '. /etc/getlino/lino_bash_aliases && go {} && . env/bin/activate &&  ls -l'.format(site_name))
        print(res)
        res = self.run_docker_command(
            '. /etc/getlino/lino_bash_aliases && go {} && source  /etc/getlino/lino_bash_aliases && . env/bin/activate  &&  pull.sh'.format(site_name))
        print(res)
        res = self.run_docker_command(
            '. /etc/getlino/lino_bash_aliases && go {} && ./make_snapshot.sh'.format(site_name))
        print(res)
        # Need to wait 10 sec until the supervisor finish restarting
        time.sleep(10)
        res = self.run_docker_command(
            '/usr/local/bin/healthcheck.sh')
        self.assertNotIn('Error', res)

    def do_test_developer_env(self, application):
        """

        Test the instrucations written on
        https://www.lino-framework.org/dev/install/index.html

        """
        site_name = "{}1".format(application)
        self.run_docker_command(
            'mkdir ~/lino && virtualenv -p python3 ~/lino/env')
        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && pip3 install -e . ')
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino configure --batch --db-engine postgresql')
        self.assertIn('getlino configure completed', res)
        # print(self.run_docker_command(container, "cat ~/.lino_bash_aliases"))
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino startsite {} {} --batch --dev-repos "lino xl noi"'.format(application, site_name))
        self.assertIn(
            'The new site {} has been created.'.format(site_name), res)
        res = self.run_docker_command(
        res=self.run_docker_command(
            '. ~/.lino_bash_aliases && go {} && . env/bin/activate && ls -l'.format(site_name))
        print(res)
        res=self.run_docker_command(
            '. ~/.lino_bash_aliases && go {} && . env/bin/activate && pull.sh'.format(site_name))
        print(res)

    def test_contributor_env(self, application):
        """

        Test the instrucations written on
        https://www.lino-framework.org/team/index.html

        """
        site_name="{}1".format(application)
        self.run_docker_command(
            'mkdir ~/lino && virtualenv -p python3 ~/lino/env')
        res=self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        res=self.run_docker_command(
            '. ~/lino/env/bin/activate && pip3 install -e . ')
        self.assertIn("Installing collected packages:", res)
        res=self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino configure --clone --devtools --redis --batch ')
        self.assertIn('getlino configure completed', res)
        # print(self.run_docker_command(container, "cat ~/.lino_bash_aliases"))
        res=self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino startsite {} {} --batch'.format(application, site_name))
        self.assertIn(
            'The new site {} has been created.'.format(site_name), res)
        res=self.run_docker_command(
            '. ~/.lino_bash_aliases && go {} && . env/bin/activate && ls -l'.format((site_name)))
        print(res)
        res=self.run_docker_command(
            '. ~/.lino_bash_aliases && go {} && . env/bin/activate && pull.sh'.format(site_name))
        print(res)

    def test_startsite_sites(self):
        tested_applications=['cosi', 'noi', 'avanti']
        for application in tested_applications:
            self.do_test_production_server(application)
            self.do_test_developer_env(application)
            self.test_contributor_env(application)

class UbuntuDockerTest(DockerTestMixin, TestCase):
    docker_tag="getlino_debian"

class DebianDockerTest(DockerTestMixin, TestCase):
    docker_tag="getlino_ubuntu"
