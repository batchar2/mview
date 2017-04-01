"""
Реализация обращений к БД через "кэш"

В случае отсутствия данных в кеше - идет обращение к БД
"""

import sqlalchemy as sql

from sqlalchemy.ext.declarative import declarative_base

from settings import SETTINGS

Base = sql.ext.declarative.declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = sql.Column(sql.Integer, primary_key=True)
	username = sql.Column(sql.String)
	password = sql.Column(sql.String)
	is_active = sql.Column(sql.Boolean, default=False)


	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.is_active = True

engine = create_engine(SETTINGS['DATABASE']['ENGINE'])
Base.metadata.create_all(engine)



class SystemUser:
	def __init__(self):
		engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


	def isUserExist(self, username, password):
		pass