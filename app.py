"""
Simple "Hello, World" application using Flask
"""

import flask
from flask.templating import render_template
from mbta_helper import find_stop_near
app = flask.Flask(__name__)


@app.route('/', methods = ['POST','GET'])
def index():
    if flask.request.method == "POST":
        user = flask.request.form["Place"]
        return flask.render_template('result.html', value = user, Place = find_stop_near(user))
    else:
        return render_template('index.html')

    


if __name__ == '__main__':
    app.run(debug=True)


