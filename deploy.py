import copy
import imp
import logging
import optparse
import subprocess
import sys

try:
    imp.find_module('salt')
except ImportError:
    subprocess.call([
        sys.executable, "-m", "pip", "install", "--verbose",
        "git+https://github.com/saltstack/salt.git@v2018.3.2"
    ])

import salt.cli.ssh
import salt.returners.local_cache
import yaml


class Playground(salt.utils.parsers.SaltSSHOptionParser):
    def __init__(self):
        super().__init__()
        playground_group = optparse.OptionGroup(
            self, 'Playground Options',
            'Parameters for the playground deployment.')
        playground_group.add_option(
            '--masters',
            dest='playground_master_nodes',
            help='List of master nodes IPs')
        playground_group.add_option(
            '--slaves',
            dest='playground_slave_nodes',
            help='List of slave nodes IPs')
        playground_group.add_option(
            '--jenkins',
            dest='playground_jenkins_node',
            help='Jenkins node IP')
        self.add_option_group(playground_group)
        self.log = logging.getLogger(__name__)

    def _mixin_after_parsed(self):
        if not self.options.playground_master_nodes:
            self.error(
                'Please provide playground master nodes IPs with --masters option'
            )
        if not self.options.playground_slave_nodes:
            self.error(
                'Please provide playground slave nodes IPs with --slaves option'
            )
        if not self.options.playground_jenkins_node:
            self.error(
                'Please provide playground Jenkins node IP with --jenkins option'
            )
        if not self.options.ssh_priv:
            self.error(
                'Please provide path to SSH private key with --priv option')

    def check(self, result, nodes, *keys):
        path = ""
        for i in nodes:
            path += i
            if result is None or i not in result:
                self.log.error('Unable to find path %s', path)
                return False
            node_result = result[i]
            # check keys
            for i in keys[:-1]:
                path += '.' + i
                if i not in node_result:
                    self.log.error('Unable to find path %s', path)
                    return False
                node_result = node_result[i]
            # check result
            if str(node_result) != str(keys[-1]):
                self.log.error('Expected value %s in path %s:%s', keys[-1],
                               path, node_result)
                return False
        return True

    def process_config_dir(self):
        if self.options.config_dir == '/etc/salt':
            self.options.config_dir = 'etc/salt'
        super(Playground, self).process_config_dir()

    process_config_dir._mixin_prio_ = salt.utils.parsers.ConfigDirMixIn._mixin_prio_

    def parse_args(self, args=None, values=None):
        # remove SaltSSHOptionParser validation
        self._mixin_after_parsed_funcs = [
            x for x in self._mixin_after_parsed_funcs
            if not x.__qualname__.startswith("SaltSSHOptionParser")
        ]
        super(Playground, self).parse_args(args, values)

    def prepare_config(self):
        self.config[
            'playground_master_nodes'] = self.options.playground_master_nodes.split(
                ',')
        self.config[
            'playground_slave_nodes'] = self.options.playground_slave_nodes.split(
                ',')
        self.config[
            'playground_jenkins_node'] = self.options.playground_jenkins_node

    def prepare_roster(self):
        roster = {}
        with open("etc/salt/roster.template", 'r') as stream:
            template = yaml.load(stream)
            zk_grains = ','.join(
                i + ':2181' for i in self.config['playground_master_nodes'])
            for i in self.config['playground_slave_nodes']:
                self.log.info("Add %s to slave nodes", i)
                roster[i] = template['NODE_NAME']
                roster[i]['minion_opts'] = {
                    'grains': {
                        'role': ['slave'],
                        'zk': zk_grains
                    }
                }
                roster[i]['priv'] = self.config['ssh_priv']
            for i in self.config['playground_master_nodes']:
                self.log.info("Add %s to master nodes", i)
                if not roster[i]:
                    roster[i] = template['NODE_NAME']
                    roster[i]['minion_opts'] = {
                        'grains': {
                            'role': ['master'],
                            'zk': zk_grains
                        }
                    }
                    roster[i]['priv'] = self.config['ssh_priv']
                else:
                    roster[i].setdefault('minion_opts', {}).setdefault(
                        'grains', {}).setdefault('role', []).append('master')
            roster.setdefault(self.config['playground_jenkins_node'],
                              {}).setdefault('minion_opts', {}).setdefault(
                                  'grains',
                                  {}).setdefault('role', []).append('jenkins')
        with open("etc/salt/roster", 'w') as stream:
            yaml.dump(roster, stream, allow_unicode=True)
        # remove SSH private key to aviod key deployment invocation
        self.config.pop('ssh_priv', None)
        return self.config['playground_master_nodes'], self.config[
            'playground_slave_nodes']

    def step(self, description, *command):
        return self.step_raw(description, False, *command)

    def step_raw(self, description, raw_flag, *command):
        self.log.info("#" * 10 + " %s", description)
        config = copy.deepcopy(self.config)
        if raw_flag:
            config['raw_shell'] = True
        config['tgt'] = command[0]
        config['argv'] = command[1:]
        ssh = salt.client.ssh.SSH(config)
        prep_jid = '{0}.prep_jid'.format(ssh.opts['master_job_cache'])
        get_jid = '{0}.get_jid'.format(ssh.opts['master_job_cache'])
        jid = ssh.returners[prep_jid]()
        try:
            ssh.run(jid)
        except SystemExit:
            pass
        return ssh.returners[get_jid](jid)

    def run(self):
        self.parse_args()
        self.prepare_config()
        masters, slaves = self.prepare_roster()
        # self.step_raw(
        #     "Install python 3 for Debian based environment", True, "*",
        #     "which python3 || apt-get -y install python36 || apt-get -y install python35"
        # )
        # self.step_raw(
        #     "Install python 3 for RH based environment", True, "*",
        #     "which python3 || " +
        #     "(yum -y install python36; ln -s /usr/bin/python36 /usr/bin/python3) ||"
        #     +
        #     "(yum -y install python35; ln -s /usr/bin/python35 /usr/bin/python3)"
        # )
        # self.step_raw("Install PIP for python 3", True, "*",
        #               "curl https://bootstrap.pypa.io/get-pip.py | python3")
        result = self.step("Test connection", "*", "test.ping")
        if not self.check(result, masters, 'return', 'return', 'True'):
            sys.exit("Unable to validate connection")
        result = self.step("Setup environment", "*", "state.highstate", "pillar={start: true}")
        if not self.check(result, masters, 'return', 'retcode', 0):
            sys.exit("Unable to setup masters environment")
        self.summary()

    def summary(self):
        print("\n\n" + "#" * 10 + " Summary\n\n")
        print("Mesos: {}".format(" ".join("http://{}:5050/".format(i) for i in self.config['playground_master_nodes'])))
        print("Marathon: {}".format(" ".join("http://{}:8080/".format(i) for i in self.config['playground_master_nodes'])))
        print("Jenkins: {}".format("http://{}:8081/".format(self.config['playground_jenkins_node'])))
        print("\n\nRun tests to validate config\n\n")


if __name__ == "__main__":
    playground = Playground()
    playground.run()
