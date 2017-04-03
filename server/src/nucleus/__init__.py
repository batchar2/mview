import os
import sys


from .settings import SETTINGS

# Первичная настройка пути до пакета сервера
abspath = os.path.abspath(SETTINGS['PACKET_HEADERS_PAKET_PATH'])
sys.path.append(abspath)

# настройка пути до обработчиков сетевых пакетов
abspath = os.path.abspath(SETTINGS['PACKET_IDENTITY_PATH'])
sys.path.append(abspath)


from .nucleus import Nucleus