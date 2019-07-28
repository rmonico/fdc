from di_container.injector import Inject

import subprocess
import os


class GitWrapperFactory(object):

    def __init__(self):
        self._configs = Inject('app configuration')
        self._logger = Inject('logger')

    @staticmethod
    def get_external_resources():
        return [{'name': 'git wrapper', 'creator': GitWrapperFactory.create_wrapper}]

    def create_wrapper(self):
        return GitWrapper()


class GitWrapper(object):

    def __init__(self):
        self._git_binary = self._get_git_binary()

    @staticmethod
    def _get_git_binary():
        p = subprocess.run(['which', 'git'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.returncode != 0:
            raise GitWrapperException('git binary not found in PATH')

        output = p.stdout.decode().split('\n')

        return output[0]

    def _git(self, *args):
        return subprocess.run([self._git_binary] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def repository_exists_at_folder(self, folder):
        current_directory = os.getcwd()

        os.chdir(folder)

        process = self._git('status')

        os.chdir(current_directory)

        return process.returncode == 0


class GitWrapperException(Exception):
    pass
