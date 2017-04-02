import ctypes

#from .base import BaseResponse

from netpackets.network import NetworkMessage

from settings import SETTINGS

#class NetworkAuthMaker(BaseResponseMaker):
class NetworkAuthMaker:	
	def run(self, *, packet):

		answer_packet = NetworkMessage()
		answer_packet.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
		#answer_packet.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']
		answer_packet.type = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['TYPE_NOT_SECURE']
		answer_packet.body = (ctypes.c_ubyte * ctypes.sizeof(packet)).from_buffer_copy(packet)

		return answer_packet