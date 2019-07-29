from di_container.injector import Inject

import subprocess
import os


# Custom git wrapper should be created by custom factories

class GitWrapper(object):

    def __init__(self, repository_folder):
        self.repository_folder = repository_folder
        self._git_binary = self._get_git_binary()

    @staticmethod
    def _get_git_binary():
        p = subprocess.run(['which', 'git'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.returncode != 0:
            raise GitWrapperException('git binary not found in PATH')

        output = p.stdout.decode().split('\n')

        return output[0]

    def _git(self, *args):
        current_directory = os.getcwd()

        os.chdir(self.repository_folder)

        process = subprocess.run([self._git_binary] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(current_directory)

        return process

    def is_repository(self):
        return self._git('status').returncode == 0

    def init(self):
        return self._git('init', '.').returncode == 0


class GitWrapperException(Exception):
    pass
