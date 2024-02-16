#!/usr/bin/python3
"""a script that starts a Flask web application"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """display an index page with filters"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


@app.teardown_appcontext
def teardown_session(exception):
    """closes the storage session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
