from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .tables import User

from settings import SETTINGS




class MemoryCacheUser:
	""" Копия данных из БД. Храню в памяти """
	
	userid = None
	username = None
	pasword = None
	date_register = None
	date_last_activity = None
	email = None
	session_uid = None 
	
	def __init__(self, *, userid, username, password, date_register, date_last_activity, email, session_uid):
		
		self.userid = userid
		self.username = username
		self.password = password
		self.date_register = date_register
		self.date_last_activity = date_last_activity
		self.email = email
		self.session_uid = session_uid


class MemoryCache:
	"""  Реализация кэша для работы с БД. """
	def __init__(self):
		self._users_list = []

	def find_session_uuid(self, *, session_uid):
		for user in self._users_list:
			if user.session_uid == session_uid:
				return user
		return None 


class DataBase:
	"""  
	Класс реализует методы для работы с БД.
	Большинство данных дублируется в памяти (кеш) для уменьшения количества обрещений к БД
	"""
	_session = None
	
	# кэш приложения в памяти
	_memory_cache = None

	def __init__(self):
		engine = create_engine(SETTINGS['DATABASE']['ENGINE'])
		Base.metadata.bind = engine
		 
		DBSession = sessionmaker(bind=engine)
		self._session = DBSession()

		self._memory_cache = MemoryCache()


	def create_user(self, *, username, password, email):
		"""  Создание нового пользователя """
		new_user = User(username=username, password=password, email=email)
		self._commit(new_user)


	def is_valid_session(self, *, session_uuid):
		""" Проверка валидности сессии пользователя. Если существует в памяти - валидна :) """
		user = self._memory_cache.find_session_uuid(session_uid)
		if user is not None:
			return True, userid
		else:
			False, None


	def auth_user(self, username, password):
		"""  Попытка авторизовать пользователя.
			Возвращаемое значение сессия и статус попытки: session_uid, True (False)
		"""
		session_uid = '1234567890'
		return session_uid, True


	def _commit(self, data):
		self._session.add(data)
		self._session.commit


"""
# Insert a Person in the person table
new_person = Person(name='new person')
session.add(new_person)
session.commit()
 
# Insert an Address in the address table
new_address = Address(post_code='00000', person=new_person)
session.add(new_address)
session.commit()
"""