from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, session
from . import main
from .forms import NameForm
from .. import db

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'))