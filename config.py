WTF_CSRF_ENABLED = True
SECRET_KEY = 'farshid'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = postgresql://ximvvccibohdap:gmkJT0lAppHwzD_Fe0jNf6dWmO@ec2-107-20-224-236.compute-1.amazonaws.com/d34k3eiptp679u
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

