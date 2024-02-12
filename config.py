import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'HjasdfhEIOdkfakUEHFdjsfh893648^*&#%'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db/data_base.sqlite')
    STATIC_FOLDER = 'static'
