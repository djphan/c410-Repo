import sqlite3
from flask import Flask, render_template, g, redirect, url_for, request, session, flash, abort

DATABASE = 'dbschema.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'this is secret!'
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def welcome():
    return '<h1>Welcome to CMPUT 410 - Jinja Lab!</h1>'

@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        addTask(category, priority, description)
        flash('New task added successfully!')
        return redirect(url_for('task'))
    
    return render_template('show_entries.html', tasks=query_db('select * from tasks'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in :-)')
            return redirect(url_for('task'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in')
    flash('You are logged out!')
    return redirect(url_for('task'))

@app.route('/edit', methods=['POST'])
def edit():
    if not session.get('logged_in'):
        abort(401)
    editTask(request.form['category'], request.form['priority'], request.form['description'], 
        request.form['oldcategory'], request.form['oldpriority'], request.form['olddescription'])
    flash('Task was edit successfully!')
    return redirect(url_for('task'))

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get('logged_in'):
        abort(401)
    removeTask(request.form['category'], request.form['priority'], request.form['description'])
    flash('Task was deleted successfully!')
    return redirect(url_for('task'))

def addTask(category, priority, description):
    query_db('insert into tasks values(?, ?, ?)', [category, int(priority), description], one=True)
    get_db().commit()

def removeTask(category, priority, description):
    query_db('delete from tasks where category = ? and priority = ? and description = ?', [category, priority, description], one=True)
    get_db().commit()

def editTask(category, priority, description, oldcategory, oldpriority, olddescription):
    query_db('update tasks set category = ?, priority = ?, description = ? where category = ? and priority = ? and description = ?', [category, priority, description, oldcategory, oldpriority, olddescription], one=True)
    get_db().commit()

def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        db = None
        
if __name__ == '__main__':
    app.debug = True
    app.run()
