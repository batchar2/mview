#!/usr/bin/env python3

import ctypes
import socket


from io import BytesIO

from nucleus.packets import chanell_level as ch
from nucleus.packets import default_options as op

class Client:

	_sock = None
	def __init__(self):
		self._sock = socket.socket()
		self._sock.connect(('localhost', 9988))
		
	def __call__(self):
		packet = ch.ChanelLevelPacket()
		packet.magic = op.MAGIC_NUMBER
		
		print("Data size={0}".format( ctypes.sizeof(packet)))
		self._sock.send(packet)
		self._sock.close()

if __name__ == '__main__':
	client = Client()
	client()