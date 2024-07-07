import os
import sys
import click

from flask import Flask, render_template
from flask import request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy 

# different for Windows
prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'dev'

@app.cli.command() # register as a command
def forge():
    """generate fake data"""
    name = 'Leee'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Fake data created.')


@click.option('--drop', is_flag = True, help='Create after drop')
def initdb(drop):
    # initialize the database
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# use in all templates
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)  # error code
def page_not_found(e):  
    return render_template('404.html'), 404  # return template and status code

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  
        title = request.form.get('title')  
        year = request.form.get('year')
        # data validation
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  
            return redirect(url_for('index'))  
        # save form data to db
        movie = Movie(title=title, year=year)  
        db.session.add(movie)  
        db.session.commit()  
        flash('Item created.')  # created successfully
        return redirect(url_for('index'))  # redirecte to home page
    
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': 
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  

        movie.title = title  # update title
        movie.year = year  # update year
        db.session.commit()  
        flash('Item updated.')
        return redirect(url_for('index'))  

    return render_template('edit.html', movie=movie)  # new record

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  
    db.session.delete(movie)  
    db.session.commit()  
    flash('Item deleted.')
    return redirect(url_for('index'))  

class User(db.Model):  # table name: user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # table name: movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


