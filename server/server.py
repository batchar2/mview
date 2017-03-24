#!/usr/bin/env python3


"""
Реализует логику работы протокола связи.
"""
class ApplicationServer:

	def __init__(self, *, port=9988, host='127.0.0.1'):
		pass

	def run(self, *, debug=False):
		pass


"""
Реализация клиентов - каждый клиент запускается в отдельном процессе. 
Пока так, далее на мультиплексирование перетяну
"""
class UserNode:
	pass


if __name__ == '__main__':
	app = ApplicationServer(port=9988, host='0.0.0.0')

	app.run(debug=True)