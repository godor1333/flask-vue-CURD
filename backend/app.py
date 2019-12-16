import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
#from model import Book, Author, association_table


# configuration
DEBUG = False

# instantiate the app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


association_table = db.Table('association',
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'))
)


class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    association = db.relationship('Book', secondary=association_table, backref=db.backref('association'), lazy='dynamic')



class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    name_book = db.Column(db.String(20))
    value = db.Column(db.Integer)
  #  association = db.relationship('Author', secondary=association_table, backref=db.backref('association'), lazy='dynamic')


BOOKS = [ ]


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')
# for l in range(0,len(a)):
#     b = Author.query.filter_by(name=a[l].name).first()
#     print(a[l].name +':')
#     for k in b.association:
#         print(k.name_book)

#def check_value(value):

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        # db.session.refresh()
        db.update(table=Author)
        post_data = request.get_json()
        ind = uuid.uuid4().hex
       # books =
        b = Author.query.filter_by(name=post_data.get('author')).first()
        if b is None:
            b = Author(name=post_data.get('author'))
            db.session.add(b)
        for books in set([x for x in post_data.get('title').split(',')]):
            check = Book.query.filter_by(name_book=books).first()
            print(check)
            if check is None:
                check = Book(name_book=books, value=post_data.get('value'))
            print(check)
            db.session.add(check)
            b.association.append(check)
        db.session.commit()
        BOOKS.append({
            'id': ind,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'value': post_data.get('value')
        })
        response_object['message'] = 'Book added!'
    else:
        a = Author.query.all()
        for l in range(0, len(a)):
            b = Author.query.filter_by(name=a[l].name).first()
            #print(a[l].name + ':')
            s = ''
            value = 0
            n = 1
            for k in b.association:
                s = s + k.name_book+ ','
                n +=1
                value = value + k.value
                #print(k.name_book)
                #print(type(k.name_book))
            #print(s)

            BOOKS.append({
                'id': a[l].author_id,
                'title':s,
                'author':a[l].name,
                'value': value/n
            })
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    #post_data = request.get_json()
    if request.method == 'PUT':
        post_data = request.get_json()
        author_change = Author.query.filter_by(name=post_data.get('author')).first()
        print(request.get_json())
        #if author_change is None:
        #author_change.name = post_data.get('author')
        for x in post_data.get('title').split(','):
            if Book.query.filter_by(name_book=x).first() is None:
                print(x)
                l = Book(name_book=x, value=post_data.get('value'))
                author_change.association.append(l)
                db.session.commit()
                db.update(table=Author)

            else:
                author_change.association.append(Book.query.filter_by(name_book=x).first())
                db.session.commit()
                db.update(table=Author)
        #author_change.association = set([x for x in post_data.get('title').split(',')])
        #remove_book(book_id)
        #Author_new = Author(author_id=book_id, name=post_data.get('author'),)
        BOOKS.append({
            'id': book_id,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'value': post_data.get('value')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        post_data = request.get_json()
        print(book_id)
        Author.query.filter_by(author_id=book_id).delete()
        db.session.commit()
        db.update(table=Author)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Author': Author, 'Book': Book}

if __name__ == '__main__':
    app.run()