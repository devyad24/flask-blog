
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('child', __name__, url_prefix='/child')

def get_child(id, check_parent=True):
    child = get_db().execute(
        'SELECT c.id, c.firstname, c.lastname, c.age, c.gender, c.parent_id'
        ' FROM child c JOIN user u on c.parent_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if not child:
        abort(404, f"Child id {id} doesn't exist")
    if check_parent and child['parent_id'] != g.user['id']:
        abort(403)
    
    return child


@bp.route('/')
@login_required
def index():
    db = get_db()
    children = db.execute(
        'SELECT c.id, c.firstname, c.lastname, c.age, c.gender, c.parent_id'
        ' FROM child c'
        ' WHERE c.parent_id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('child/index.html', children=children)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        gender = request.form['gender']
        error = None

        if not firstname:
            error = 'First name is required.'
        elif not age:
            error = "Please specify child's age."
        elif not gender:
            error = "Please specify child's gender."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO child (firstname, lastname, age, gender, parent_id)'
                ' VALUES(?, ?, ?, ?, ?)',
                (firstname, lastname, age, gender, g.user['id'])
            )
            db.commit()
            return redirect(url_for('child.index'))

    return render_template('child/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    child = get_child(id)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        gender = request.form['gender']
        error = None

        if not firstname:
            error = "First Name is required."
        elif not age:
            error = "Age is required."
        elif not gender:
            gender = "Please specify child's gender"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE child SET firstname = ?, lastname = ?, age = ?, gender = ?'
                'WHERE id = ?',
                (firstname, lastname, age, gender, id)
            )
            db.commit()
            return redirect(url_for('child.index'))
    
    return render_template('child/update.html', child=child)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    get_child(id)

    db = get_db()
    db.execute(
        'DELETE FROM child WHERE id = ?',
        (id,)
    )
    db.commit()
    
    return redirect(url_for('child.index'))

