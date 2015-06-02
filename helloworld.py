from flask import Flask

from rulesrepo import RulesRepo


app = Flask(__name__)


@app.route('/archive')
def download_archive():
    dir = RulesRepo().get_fresh_content()
    return dir


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

