import unittest
from app import app, db, Author, Book



class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_Author(self):
        a1 = Author(name='Vasia')
        a2 = Author(name='Kek')
        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()
        self.assertEqual(a1.name, 'Vasia')
        self.assertEqual(a2.name, 'Kek')

    def test_value_check(self):
        a1 = Author(name='Vasia')
        db.session.add(a1)
        book1 = Book(name_book='asdf', value=5)
        book2 = Book(name_book='asdfasdf', value=5)
        db.session.add(book1)
        db.session.add(book2)
        a1.association.append(book1)
        a1.association.append(book2)
        self.assertEqual((book1.value +book2.value)/2, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)