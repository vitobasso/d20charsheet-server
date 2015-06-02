from flask import Flask, make_response
from github import Github


app = Flask(__name__)
USER = 'vitobasso'
REPO = 'dnd3.5-data'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('download/', defaults={'path': ''})
@app.route('download/<path:path>')
def download(path):
    g = Github()
    user = g.get_user(USER)
    repo = user.get_repo(REPO)
    file = repo.get_contents(path)
    content = file.content.decode('base64')

    response = make_response(content)
    response.headers["Content-Disposition"] = "attachment; filename=" + path
    return response


if __name__ == '__main__':
    app.run()

