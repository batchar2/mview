"""
Описание таблиц системы
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
	email = sql.Column(sql.String)
	date_register = sql.Column(sql.TIMESTAMP)
	data_last_activity = sql.Column(sql.TIMESTAMP)

	is_active = sql.Column(sql.Boolean, default=False)


	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.is_active = True

engine = sql.create_engine(SETTINGS['DATABASE']['ENGINE'])
Base.metadata.create_all(engine)

