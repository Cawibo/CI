from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello :)"


@app.route("/webhook", methods=['POST'])
def github_webhook_handler():
    print(request.form)
    return "Just reflecting data\n" + str(["{}:{}".format(x, y) for x, y in request.form.items()])


if __name__ == '__main__':
    app.run(debug=True, port=80)
