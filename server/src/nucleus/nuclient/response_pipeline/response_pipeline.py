


"""
Данный класс ответственен за генерирование ответов клиенту.
Реализованый протокол штука иерархочная: пакеты вложены друг в друга. 
Идея обработки заключается в написании обработчиков: как по цепочке (pipe)
"""

class ResponsePipeline:
	"""
	Состовляет цепочку компонентов ответственных за отправку пакетов  в ответ клиенту
	"""	
	
	# словарь. в качестве ключа команда и цепочка методов как ее надо обработать
	_pipelines = {}

	def add_pipeline(self, *, packet_type, pipeline, tail_action):
		""" Добавляет команду и цепочку методов ответственных за обработку и отправку пакета
		:param packet_type: команда (тип пакета из настроек)
		:param pipeline: список обработчиков
		:param tail_action: вызывает в конце обработки данный метод и передает ему получившиеся данные
		"""
		self._pipelines[packet_type] = {'pipeline': pipeline, 'tail_action': tail_action}

	def response(self, *, packet_type, packet):
		""" Отвечает на запрос:
		:param packet_type: тип пакета
		:param packet: подготовленый пакет, который нужно обернуть
		"""
		if packet_type in self._pipelines:
			pipeline = self._pipelines[packet_type]['pipeline']
			tail_action = self._pipelines[packet_type]['tail_action']

			# Обрабатываем по порядку элементы цепочки
			for action in pipeline:
				packet = action.run(packet=packet)

			# вызываем заключительный обработчик
			tail_action(packet)

