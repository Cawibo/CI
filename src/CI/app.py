from flask import Flask, request
from fs import flatten_data, get_paths, clone_repo, setup_logs, run_flake8, clear_tmp
import os

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello :)"



@app.route("/webhook", methods=['POST'])
def github_webhook_handler():
    content = request.get_json(silent=True)
    
    if content['pull_request']:
        data = flatten_data(content)
        tmp, path_to_logs, path_to_src = get_paths(data)

        clone_repo(data)
        setup_logs(path_to_logs)
        res = run_flake8(data, path_to_src, path_to_logs+data['timestamp'])
        clear_tmp(tmp+data['repo'])

    return ""


if __name__ == '__main__':
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('logs'):
        os.mkdir('logs')
    app.run(host='0.0.0.0', debug=True, port=83)
