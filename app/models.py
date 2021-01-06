from app.database import db
import hashlib
from hashlib import sha256
from app.classes import Uploads
import string
from random import choice

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def get_id(self):
        return self.id

    def get_username():
        return self.username
    
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def create_user(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def login_attempt(self, username, password):
        query = self.custom_query('username', username)
        if (not query) or (query.password != self.hash_password(password)):
            return False
        return query


class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(300), nullable=False)
    explore = db.Column(db.String(10), nullable=True)
    link_code = db.Column(db.String(12), nullable=False)
    items = db.relationship('Item', backref='/items')
    star = db.relationship('Star', backref='/stared')

    def add_list(self, list_items):
        db.session.add(self)
        db.session.commit()

        items = list_items.split('\n')
        output = [x.replace('\r', '') for x in items]

        for i in output:
            Item(item=i, list_id=self.id).add_item()

        return self.link_code

    def update_list_title(self, user, code, title):
        query = self.query.filter_by(user=user, link_code=code).first()
        if not query:
            return False
        query.name = title
        db.session.commit()
        return query

    def check_correct_user(self, user, code):
        if not self.query.filter_by(user=user, link_code=code).first():
            return False
        return True

    @staticmethod
    def generate_link_code(StringLength=12):
        code = string.ascii_letters + string.digits
        return ''.join(choice(code) for i in range(StringLength))

    def query_list(self, user, link_code):
        return self.query.filter_by(user=user, link_code=link_code).first()

    def return_all_lists(self, user):
        return self.query.filter_by(user=user).all()

    def explore_lists(self):
        return self.query.filter_by(explore='y').all()

class Item(db.Model):
    __tablename__ = 'list_items'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(300), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def add_item(self):
        db.session.add(self)
        db.session.commit()
        return self

    def add_many(self, list_items):
        items = list_items.split('\n')
        output = [x.replace('\r', '') for x in items]

        for i in output:
            Item(item=i, list_id=self.list_id).add_item()
        return True
          
    def delete_item(self, list_id, id):
        query = self.query.filter_by(list_id=list_id, id=id).first()
        if not query:
            return False
        db.session.delete(query)
        db.session.commit()
        return True

class Star(db.Model):
    __tablename__ = 'starred'
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()