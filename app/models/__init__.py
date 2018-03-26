import ast
import hashlib
import uuid

import arrow

from flask import current_app
from flask import request
from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .. import login_manager


class Permission(object):
    """
    A specific permission task is given a bit position.  Eight tasks are
    avalible because there are eight bits in a byte.
    """
    VIEW = int('00000001', 2)
    EDIT = int('00000010', 2)
    INSERT = int('00000100', 2)
    DELETE = int('00001000', 2)
    # TASK_TBD = int('00010000', 2)
    # TASK_TBD = int('00100000', 2)
    # TASK_TBD = int('01000000', 2)
    ADMINISTER = int('10000000', 2)  # 0xff


class Base(object):
    """docstring for Base Model"""
    key = str(uuid.uuid4())

    def __init__(self, *args, **kwargs):

        self.key = str(uuid.uuid4())
        super(Base, self).__init__(*args, **kwargs)

    def save(self):
        __tablename__ = self.__tablename__

        count = current_app.redis.lpush(
            __tablename__, vars(self))

        if count:
            return self

    @classmethod
    def get(cls, key, default=None):

        __tablename__ = cls.__tablename__
        table = current_app.redis.lrange(__tablename__, 0, -1)

        if not table:
            return default
        print(len(table))
        for record in table:

            record = ast.literal_eval(record)

            if record.get('key', None) and record['key'] == key:
                obj = cls(**record)
                obj.key = key
                return obj

        return default


class Role(Base):
    __tablename__ = 'roles'

    def __init__(self, name, default=False, *args, **kwargs):
        super(Role, self).__init__()
        self.name = name
        self.default = default
        self.permissions = {}
        self.users = []

    @staticmethod
    def insert_roles():
        """Update or create all Roles."""
        roles = {
            'Sales': (Permission.VIEW |
                      Permission.INSERT, True),
            'Manager': (Permission.VIEW |
                        Permission.EDIT |
                        Permission.INSERT, False),
            'Administrator': (int('11111111', 2), False)
        }
        for r in roles:
            role = Role.get(name=r)
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.save()

    @staticmethod
    def add_user(role_name, user):
        role = Role.get(name=role_name)
        role.users.append(user)

        role.save

    def __str__(self):
        return '<Role %r>' % self.name


class User(UserMixin, Base):
    __tablename__ = 'users'

    def __init__(self, email, first_name, last_name,
                 role=None, *args, **kwargs):

        super(User, self).__init__()

        self.email = email.strip()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.password_hash = kwargs.get('password_hash', None)
        self.role = role
        self.about_me = kwargs.get('about_me', '').strip()
        self.avatar_hash = kwargs.get('avatar_hash', None)
        self.authenticated = True
        # if self.role is None:
        #     if self.email in current_app.config['DASHBOARD_ADMIN']:
        #         self.role = Role.get(permissions=0xff)
        #     if self.role is None:
        #         self.role = Role.get(default=True)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @staticmethod
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    @staticmethod
    def is_active(self):
        """True, as all users are active."""
        return True

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        Generate a JSON Web Signature token with an expiration.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.key})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.key})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except ValueError:
            return False
        if data.get('reset') != self.key:
            return False
        self.password = new_password
        self.save()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.key, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except ValueError:
            return False
        if data.get('change_email') != self.key:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.get(email=new_email) is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        self.save()
        return True

    @classmethod
    def get_email(cls, email, default=None):

        __tablename__ = cls.__tablename__
        table = current_app.redis.lrange(__tablename__, 0, -1)

        if not table:
            return default

        for record in table:
            record = ast.literal_eval(record)

            if record.get('email', None) and record['email'] == email:
                obj = cls(**record)
                obj.key = record.get('key')
                return obj

        return default

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def get_id(self):
        return self.key

    def ping(self):
        self.last_seen = str(arrow.now('Africa/Lagos'))
        self.save()

    def gravatar(self, size=100, default='identicon', rating='g'):
        # match the security of the client request
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'

        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __str__(self):
        return '<User %r>' % self.key


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# Register AnonymousUser as the class assigned to 'current_user' when the user
# is not logged in.  This will enable the app to call 'current_user.can()'
# without having to first check if the user is logged in
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    Callback function required by Flask-Login that loads a User, given the
    User identifier.  Returns User object or None.
    """

    return User.get(user_id)
