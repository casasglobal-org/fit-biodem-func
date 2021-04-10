from flask import render_template

from .user_data import create_app

app = create_app()


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
