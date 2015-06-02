import urllib
import tarfile
import os

import github


def download_tar(url, path):
    opener = urllib.URLopener()
    opener.retrieve(url, path)


def extract_tar(path):
    tar = tarfile.open(path)
    dir = os.path.dirname(path)
    tar.extractall(dir)
    tar.close()


class RulesRepo():

    def __init__(self):
        g = github.Github()
        self.user = g.get_user('vitobasso')
        self.repo = self.user.get_repo('dnd3.5-data')
        default_branch = self.repo.default_branch
        self.branch = self.repo.get_branch(default_branch)

    def last_commit_timestamp(self):
        date = self.branch.commit.commit.committer.date
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def temp_dir_path(self):
        cwd = os.getcwd()
        timestamp = self.last_commit_timestamp()
        path = os.path.join(cwd, 'temp', timestamp)
        return path

    def download_new_archive(self, dir):
        os.makedirs(dir)
        url = self.repo.get_archive_link('tarball')
        path = os.path.join(dir, 'rules-source.tar.gz')
        download_tar(url, path)
        extract_tar(path)

    def get_fresh_content(self):
        dir = self.temp_dir_path()
        exists = os.path.isdir(dir)
        if not exists:
            self.download_new_archive(dir)
        return dir
