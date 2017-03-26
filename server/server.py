#!/usr/bin/env python3

from nucleus import Nucleus




if __name__ == '__main__':
    nucl = Nucleus(port=9988, host='0.0.0.0', debug=True)

    nucl()