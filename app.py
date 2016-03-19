from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


class Config(object):
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@db:3306/blog'.format(os.getenv('MYSQL_ROOT_PASSWORD'))
    # 输出调试sql语句
    SQLALCHEMY_ECHO = True


app.config.from_object(Config)
db = SQLAlchemy(app)


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __str__(self):
        return self.name


@app.route('/', defaults={'name': 'default_name'})
@app.route('/<string:name>')
def index(name):
    db.create_all()
    test = Test()
    test.name = name
    db.session.add(test)
    db.session.commit()
    return '{}'.format(Test.query.count())


if __name__ == '__main__':
    app.run()
