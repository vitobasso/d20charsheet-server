from flask import Flask, make_response, redirect
from github import Github


app = Flask(__name__)
USER = 'vitobasso'
REPO = 'dnd3.5-data'


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_repo():
    g = Github()
    user = g.get_user(USER)
    repo = user.get_repo(REPO)
    return repo


def get_attached_response(file_content, file_name):
    response = make_response(file_content)
    response.headers["Content-Disposition"] = "attachment; filename=" + file_name
    return response


@app.route('/file/', defaults={'path': ''})
@app.route('/file/<path:path>')
def download_path(path):
    repo = get_repo()
    file = repo.get_contents(path)
    content = file.content.decode('base64')
    return get_attached_response(content, path)


@app.route('/archive')
def download_archive():
    repo = get_repo()
    archive_url = repo.get_archive_link('tarball')
    return redirect(archive_url)


if __name__ == '__main__':
    app.run()

