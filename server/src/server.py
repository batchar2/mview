#!/usr/bin/env python3

from nucleus import Nucleus


from nucleus.settings import SETTINGS 

if __name__ == '__main__':
    
    packet_max_size = SETTINGS['PROTOCOLS']['PACKET_SIZE']
    nucl = Nucleus(port=9988, host='0.0.0.0', debug=True, settings=SETTINGS)

    nucl()