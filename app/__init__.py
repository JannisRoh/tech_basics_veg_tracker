from config import Config

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Initialization of the app itself, the config and libraries used.
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app import routes, models

@app.before_first_request
def init_db():
    db.create_all

if __name__ == '__main__':
    app.run()
