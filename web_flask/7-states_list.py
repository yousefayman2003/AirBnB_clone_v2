#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """displays states listed in alphabetical order"""
    states = list(storage.all(State).values())
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
