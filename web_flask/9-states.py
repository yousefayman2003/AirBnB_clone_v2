#!/usr/bin/python3
"""a scripts that starts a Flask web application"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """display the states and cities in order"""
    states = storage.all("State")
    if state_id is not None:
        state_id = 'State.' + state_id
    return render_template('9-states.html', states=states, state_id=state_id)


@app.teardown_appcontext
def teardown_session(exception):
    """closes the storage session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
