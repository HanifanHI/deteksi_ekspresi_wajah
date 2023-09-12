import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    HOST = "localhost"
    DATABASE = "final_bigproject"
    USERNAME = "root"
    PASSWORD = ""
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
        USERNAME+':'+PASSWORD+'@'+HOST+'/'+DATABASE
    # SQLALCHEMY_DATABASE_URI = 'postgres://irrmeclqiwslnq:f0dcddd75f3db9f0749a957b7e54ceb90d73db00100afd69f0ea0cec81917180@ec2-52-44-80-40.compute-1.amazonaws.com:5432/dcj66kgq9q2mpo'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
