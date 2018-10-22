from LoginHub import AppConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__user = AppConfig.get("MYSQL_USER")
__password = AppConfig.get("MYSQL_PASSWORD")
__address = AppConfig.get("MYSQL_HOST")
__port = AppConfig.get("MYSQL_PORT", "3306")
__dbname = AppConfig.get("MYSQL_DATABASE")

__db_uri = "mysql+pymysql://" + __user + ":" + __password + "@" + __address + ":" + __port + "/" + __dbname

Engine = create_engine(__db_uri)

__session = sessionmaker(bind=Engine)
Session = scoped_session(__session)
