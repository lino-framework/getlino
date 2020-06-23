# Copyright 2019-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from os.path import dirname, join
import time
from atelier.test import TestCase
import docker
import getlino

client = docker.from_env()


class DockerTestMixin:
    docker_tag = None
    tested_applications = ['cosi', 'noi', 'avanti']

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

    def test_production_server(self):
        """

        Test the instrucations written on
        https://www.lino-framework.org/admin/install.html

        """
        # load bash aliases
        # res = self.run_docker_command(
        #    container, 'source /etc/getlino/lino_bash_aliases')
        res = self.run_docker_command('ls -l')
        self.assertIn('setup.py', res)
        # create and activate a master virtualenv
        self.run_docker_command('sudo mkdir -p /usr/local/lino/shared/env')
        self.run_docker_command(
            'cd /usr/local/lino/shared/env && sudo chown root:www-data . && sudo chmod g+ws . && virtualenv -p python3 master')
        mastercmd = ". /usr/local/lino/shared/env/master/bin/activate && {}"
        res = self.run_docker_command(mastercmd.format('sudo pip3 install -e .'))
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command('ls -l')
        self.assertIn('setup.py', res)
        # print(self.run_docker_command(container, "sudo cat /etc/getlino/lino_bash_aliases"))
        res = self.run_docker_command(
            mastercmd.format('sudo getlino configure --batch --db-engine postgresql --monit'))
        self.assertIn('getlino configure completed', res)

        for application in self.tested_applications:
            site_name = "{}1".format(application)
            cmd = 'sudo getlino startsite {} {} --batch'.format(application, site_name)
            res = self.run_docker_command(mastercmd.format(cmd))
            self.assertIn(
                'The new site {} has been created.'.format(site_name), res)
            cmdtpl = ". /etc/getlino/lino_bash_aliases && go {} && . env/bin/activate".format(site_name)
            cmdtpl += " && {}"
            # res = self.run_docker_command(cmdtpl.format('ls -l'))
            # print(res)
            # res = self.run_docker_command(cmdtpl.format('pull.sh'))
            # print(res)
            res = self.run_docker_command(cmdtpl.format('python manage.py prep --noinput'))
            print(res)
            res = self.run_docker_command(cmdtpl.format('./make_snapshot.sh'))
            print(res)
            # Wait 10 sec for supervisor to finish restarting
            time.sleep(10)
            res = self.run_docker_command('/usr/local/bin/healthcheck.sh')
            self.assertNotIn('Error', res)

            cmd = '/etc/cron.daily/make_snapshot_{}.sh'.format(site_name)
            res = self.run_docker_command(cmd)
            print(res)


    def test_developer_env(self):
        """

        Test the instructions written on
        https://www.lino-framework.org/dev/install/index.html

        """
        venv = '~/lino/env'
        self.run_docker_command('mkdir ~/lino && virtualenv -p python3 {}'.format(venv))
        res = self.run_docker_command('ls -l')
        self.assertIn('setup.py', res)
        cmdtpl = '. {}/bin/activate'.format(venv)
        cmdtpl += " && {}"
        res = self.run_docker_command(cmdtpl.format('pip3 install -e . '))
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(
            cmdtpl.format('getlino configure --batch --db-engine postgresql'))
        self.assertIn('getlino configure completed', res)
        # print(self.run_docker_command(container, "cat ~/.lino_bash_aliases"))

        for app in self.tested_applications:
            site_name = "{}1".format(app)
            cmd = 'getlino startsite {} {} --batch --dev-repos "lino xl {}"'.format(
                app, site_name, app)
            res = self.run_docker_command(cmdtpl.format(cmd))
            self.assertIn(
                'The new site {} has been created.'.format(site_name), res)
        # res = self.run_docker_command('. ~/.lino_bash_aliases && go {} && . env/bin/activate && ls -l'.format(site_name))
        # print(res)
        # res=self.run_docker_command('. ~/.lino_bash_aliases && go {} && . env/bin/activate && pull.sh'.format(site_name))
        # print(res)

    def do_test_contributor_env(self, application):
        """

        Test the instrucations written on
        https://www.lino-framework.org/team/index.html

        """

        # TODO: this does not yet work. before going on, we need to meditate on
        # the docs as well.
        # https://www.lino-framework.org/team/install/index.html

        site_name = "{}1".format(application)
        self.run_docker_command(
            'mkdir ~/lino && virtualenv -p python3 ~/lino/env')
        res=self.run_docker_command('ls -l')
        self.assertIn('setup.py', res)
        self.run_docker_command("touch ~/.bash_aliases")
        cmdtpl = ". ~/lino/env/bin/activate && . ~/.bash_aliases && {}"
        res = self.run_docker_command(cmdtpl.format('pip3 install -e . '))
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(cmdtpl.format(
            'getlino configure --clone --devtools --redis --batch '))
        self.assertIn('getlino configure completed', res)
        # print(self.run_docker_command(container, "cat ~/.lino_bash_aliases"))

        for application in self.tested_applications:
            site_name = "{}1".format(application)
            res = self.run_docker_command(cmdtpl.format(
                'getlino startsite {} {} --batch'.format(application, site_name)))
            self.assertIn(
                'The new site {} has been created.'.format(site_name), res)
            res=self.run_docker_command(cmdtpl.format(
                'go {} && . env/bin/activate && ls -l'.format(site_name)))
            print(res)
            res=self.run_docker_command(cmdtpl.format(
                '&& go {} && . env/bin/activate && pull.sh'.format(site_name)))
            print(res)

    def skipped_test_contributor_env(self):
        for application in self.tested_applications:
            self.do_test_contributor_env(application)

class UbuntuDockerTest(DockerTestMixin, TestCase):
    docker_tag="getlino_debian"

class DebianDockerTest(DockerTestMixin, TestCase):
    docker_tag="getlino_ubuntu"
