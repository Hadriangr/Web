import dis


with open('settings.cpython-311.pyc', 'rb') as archivo:
    bytecode = archivo.read()

dis.dis(bytecode)