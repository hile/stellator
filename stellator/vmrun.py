"""
Wrap vmrun calls
"""

import os
from subprocess import Popen, PIPE

VMRUN_RELATIVE_PATH = 'Contents/Library/vmrun'


class VMRunError(Exception):
    pass


class VMRunWrapper(object):
    """Wrap vmrun

    Execute some vmrun commands. Just what we need.
    """

    def __init__(self, config):
        self.path = os.path.join(config['application_path'], VMRUN_RELATIVE_PATH)
        if not os.access(self.path, os.X_OK):
            raise VMRunError('Not executable: {}'.format(self.path))

    def __run__(self, args):
        command = [self.path] + args
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr

    def __format_stdout_stderr__(self, stdout, stderr):
        stdout = str(stdout, 'utf-8').rstrip()
        stderr = str(stderr, 'utf-8').rstrip()
        message = ''
        if stdout:
            message += '{}\n'.format(stdout)
        if stderr:
            message += '{}\n'.format(stderr)
        return message

    def running_vms(self):
        rv, stdout, stderr = self.__run__(['list'])
        if rv != 0:
            raise VMRunError('Error running vmrun list: {}'.format(stderr))

        stdout = str(stdout, 'utf-8').rstrip()
        return stdout.splitlines()[1:]

    def start(self, vmx_path, headless=False):
        if headless:
            rv, stdout, stderr = self.__run__(['start', vmx_path, 'nogui'])
        else:
            rv, stdout, stderr = self.__run__(['start', vmx_path])

        if rv != 0:
            raise VMRunError('Error starting {}: {}'.format(
                vmx_path,
                self.__format_stdout_stderr__(stdout, stderr)
            ))

    def suspend(self, vmx_path):
        rv, stdout, stderr = self.__run__(['suspend', vmx_path])

        if rv != 0:
            raise VMRunError('Error suspending {}: {}'.format(
                vmx_path,
                self.__format_stdout_stderr__(stdout, stderr)
            ))

    def stop(self, vmx_path):
        rv, stdout, stderr = self.__run__(['stop', vmx_path])

        if rv != 0:
            raise VMRunError('Error stopping {}: {}'.format(
                vmx_path,
                self.__format_stdout_stderr__(stdout, stderr)
            ))
