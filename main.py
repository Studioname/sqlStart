from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db = sqlite3.connect("books-collection.db")
#
# cursor = db.cursor()
#
# cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(2, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(240), unique=True, nullable=False)
    book_author = db.Column(db.String(240), unique=False, nullable=False)
    rating = db.Column(db.Float(4), unique=False, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.book_name

db.create_all()

all_books = []

# #add an entry
# harry_potter = Book(book_name="Harry Potter", book_author="JK Rowling", rating="7.35")
# db.session.add(harry_potter)
# db.session.commit()
#
# #reads all records
# list_of_books = Book.query.all()
# print(list_of_books)
#
# #find a particular record by query
# book_to_update = Book.query.filter_by(book_name='Harry Potter').first()
#
# #update a record by query
# book_to_update.book_name = "Harry Potter and the Chamber of sdfada"
# db.session.commit()
#
# #delete a record by primary key
# book_id = 1
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()

@app.route('/', methods=['GET'])
def home():
    list_of_books = Book.query.all()
    return render_template('index.html', books=list_of_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_entry = Book(book_name = request.form["book_name"], book_author = request.form["book_author"], rating= request.form["rating"])
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["edit_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_to_update = Book.query.get(book_id)
    return render_template("edit.html", book=book_to_update)

@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

# @app.route("/edit", methods=['POST', 'GET'])
# def edit():
#     book_id = request.form["id"]
#     book_to_update = Book.query.get(book_id)
#     if request.method == "POST":
#         book_to_update.rating = request.form["edit_rating"]
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template("edit.html", book=book_to_update)


if __name__ == "__main__":
    app.run(debug=True)

