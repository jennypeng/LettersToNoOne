# -*- coding: utf-8 -*-
import datetime
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create app
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE='flaskr.db',
    DATABASE='letters.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('APP_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('letters.db')
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/write')
def write():
    return render_template('write.html')
@app.route('/read')
def read():
    db = get_db()
    cur = db.execute('select text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    date = datetime.datetime.now().strftime("%B %d, %Y (%H:%M:%S)")
    print(date);
    db.execute('insert into entries (date, text) values (?, ?)', [date, request.form['text']])
    db.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    init_db()
    app.run()