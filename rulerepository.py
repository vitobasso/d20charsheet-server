import urllib
import tarfile
import os

import github

from rulefilter import RuleFilter
from commons import src_name


repo_name = 'dnd3.5-data'
user_name = 'vitobasso'


class RulesRepository():

    def last_commit_timestamp(self):
        date = self.branch.commit.commit.committer.date
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def temp_dir_path(self):
        cwd = os.getcwd()
        timestamp = self.last_commit_timestamp()
        path = os.path.join(cwd, 'temp', timestamp)
        return path

    def __init__(self):
        g = github.Github()
        self.user = g.get_user(user_name)
        self.repo = self.user.get_repo(repo_name)
        default_branch = self.repo.default_branch
        self.branch = self.repo.get_branch(default_branch)
        self.basedir = self.temp_dir_path()
        tar_name = src_name + '.tar.gz'
        self.tarpath = os.path.join(self.basedir, tar_name)

    def download_tar(self):
        url = self.repo.get_archive_link('tarball')
        opener = urllib.URLopener()
        opener.retrieve(url, self.tarpath)

    def extract_tar(self):
        tar = tarfile.open(self.tarpath)
        tar.extractall(self.basedir)
        tar.close()

    def find_extracted_folder(self):
        dirprefix = user_name + '-' + repo_name
        for root, dirs, files in os.walk(self.basedir):
            for dir in dirs:
                if dir.startswith(dirprefix):
                    return dir

    def rename_extracted_folder(self):
        oldname = self.find_extracted_folder()
        oldpath = os.path.join(self.basedir, oldname)
        newpath = os.path.join(self.basedir, src_name)
        os.rename(oldpath, newpath)

    def download_new_archive(self):
        os.makedirs(self.basedir)
        self.download_tar()
        self.extract_tar()
        self.rename_extracted_folder()

    def refresh_content(self):
        exists = os.path.isdir(self.basedir)
        if not exists:
            self.download_new_archive()

    def filter(self, book_selection):
        filter = RuleFilter(self.basedir, book_selection)
        filter.filter_rule_files()
