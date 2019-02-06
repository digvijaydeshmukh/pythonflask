from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    prise = db.Column(db.String(50), nullable=False)

    def add_book(_name, _author, _prise):
        new_book = Book(name=_name, author=_author, prise=_prise)
        db.session.add(new_book)
        db.session.commit()

    def get_all_book(self):
        return Book.query.all()

    def delete_single_record(_name):
        return Book.query.filter_by(name=_name).delete()
        db.session.commit()

    def delete_all_book(self):
        return Book.query.delete()

    def __repr__(self):
        book_object = {
            'name': self.name,
            'author': self.author,
            'prise': self.prise
        }
        return json.dumps(book_object)
