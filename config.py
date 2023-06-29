import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'upfgasruigasd;vjnizpU9QNF1239831'
    """
    An if loop that stores the environment variable for the Database URL to connect with PostgreSQL or leaves the psqlURI empty, so the SQLite3 database is used when the app is run locally.
    Render uses the outdated postgres:// notation in their environment variables, this needs to be replaced with the new version, postgresql://.
    The replace function makes the if statement necessary, since including it directly, in the or statement below would cause an error when run locally.
    """
    if os.getenv('DATABASE_URL'):
        psqlURI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        psqlURI = None
    SQLALCHEMY_DATABASE_URI = psqlURI or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
