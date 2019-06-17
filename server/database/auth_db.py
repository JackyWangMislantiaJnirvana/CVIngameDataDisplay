import hashlib
import random
import string

from flask import current_app

import database


# Invite code database

def invite_code_exists(code=None) -> bool:
    db = database.get_database()

    return db.execute('SELECT * FROM invite_code where code = ?', (code,)).fetchone() is not None


def append_invite_code() -> str:
    db = database.get_database()

    code: str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    while invite_code_exists(code):
        code = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    db.execute('INSERT INTO invite_code (code) values (?)', (code,))
    db.commit()
    cid = db.execute('SELECT * FROM invite_code where code = ?', (code,)).fetchone()['id']
    return cid, code


def remove_invite_code(code):
    db = database.get_database()
    if invite_code_exists(code):
        db.execute('DELETE FROM invite_code WHERE code = ?', (code,))
        db.commit()


def get_invcode_list():
    return database.get_database().execute('SELECT * FROM invite_code').fetchall()

# User creation and login database


def get_user(username):
    return database.get_database().execute('SELECT * FROM user where username = ?', (username,)).fetchone()


def get_userlist():
    return database.get_database().execute('SELECT * FROM user').fetchall()


def set_user_description(username, desc):
    db = database.get_database()
    db.execute('UPDATE user SET description=? WHERE username=?', (desc, username))
    db.commit()


def username_exists(username):
    return get_user(username) is not None


def generate_password_hash(password) -> str:
    return hashlib.sha1((password + current_app.config['SALT']).encode('utf-8')).hexdigest()


def generate_strong_password() -> str:
    return ''.join(random.sample(string.ascii_letters + string.digits, 12))


def set_user_password(username, password):
    db = database.get_database()
    h = generate_password_hash(password)
    db.execute('UPDATE user SET password_hash=? WHERE username=?', (h, username))
    db.commit()


def is_admin(username):
    return get_user(username)['admin'] == 1


def set_admin(username: str, is_admin: bool):
    db = database.get_database()
    db.execute('UPDATE user SET admin=? WHERE username=?', (int(is_admin), username))
    db.commit()


def create_user(username, password, code, api_secret, admin=False):
    db = database.get_database()

    assert ((not username_exists(username)) and (password != '') and invite_code_exists(code))
    h = generate_password_hash(password)
    db.execute('INSERT INTO user (username, password_hash, description, api_secret, admin) values (?, ?, ?, ?, ?)',
               (username, h, '', api_secret, admin))
    db.commit()


def remove_user(username):
    db = database.get_database()

    assert username_exists(username)
    db.execute('DELETE FROM user WHERE username = ?', (username,))
    db.commit()


def validate_login(username, password) -> bool:
    db = database.get_database()

    if not username_exists(username):
        return False

    h1 = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()['password_hash']
    h2 = generate_password_hash(password)

    return h1 == h2
