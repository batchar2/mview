import ctypes

#from .base import BaseResponseMaker

from netpackets.chanel import ChanelPacket

from settings import SETTINGS

#class ChanelNotSecureMaker(BaseResponseMaker):
class ChanelNotSecureMaker:
	def run(self, *, packet):

		answer_packet = ChanelPacket()
		answer_packet.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
		answer_packet.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']
		answer_packet.type = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['TYPE_NOT_SECURE']
		answer_packet.body = (ctypes.c_ubyte * ctypes.sizeof(packet)).from_buffer_copy(packet)

		return answer_packet