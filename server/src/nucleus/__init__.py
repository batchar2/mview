import os
import sys


from .settings import SETTINGS

# Первичная настройка пути
abspath = os.path.abspath(SETTINGS['PACKET_HEADERS_PAKET_PATH'])
sys.path.append(abspath)

from .nucleus import Nucleus