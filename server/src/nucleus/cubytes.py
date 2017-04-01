"""
Преобразование сишных строк в питонячие и обратно
"""
import ctypes

def str2cubytes(string, size):
    return (ctypes.c_ubyte * size)(*[ctypes.c_ubyte(ord(char)) for char in string])

def cubutes2str(cubytes):
    symbols =  [chr(byte) for byte in cubytes]
    string = ""
    for symbol in symbols:
        string += symbol
    return string
