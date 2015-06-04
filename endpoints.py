from flask import Flask, make_response

from rulerepository import RulesRepository


app = Flask(__name__)

def get_attached_response(file_content, file_name):
    response = make_response(file_content)
    response.headers["Content-Disposition"] = "attachment; filename=" + file_name
    return response


@app.route('/rules')
def download_archive(book_selection=['6']):
    rules = RulesRepository()
    rules.refresh_content()
    rules.filter(book_selection)
    return rules.basedir


@app.route('/')
def hello_world():
    return 'Hello World!'


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('temp/logs')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


if __name__ == '__main__':
    app.run()

