import random
import serial
import serial.tools.list_ports


class Communication:
    baudrate = ''
    portName = ''
    dummyPlug = False
    ports = serial.tools.list_ports.comports()
    ser = serial.Serial()

    def __init__(self):
        self.baudrate = 9600
        print("Доступные порты (if none appear, press any letter): ")
        for port in sorted(self.ports):
            print(("{}".format(port)))
        self.portName = input("Напишите название порта (ex: /dev/ttyUSB0): ")
        try:
            self.ser = serial.Serial(self.portName, self.baudrate)
        except serial.serialutil.SerialException:
            print("Невозможно открыть: ", self.portName)
            self.dummyPlug = True
            print("Тестовый мод")

    def close(self):
        if(self.ser.isOpen()):
            self.ser.close()
        else:
            print(self.portName, " it's already closed")

    def getData(self):
        if(self.dummyMode == False):
            value = self.ser.readline()  # read line (single value) from the serial port
            decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
            # print(decoded_bytes)
            value_chain = decoded_bytes.split(",")
        else:
            value_chain = [0] + random.sample(range(0, 300), 1) + \
                [random.getrandbits(1)] + random.sample(range(0, 20), 8)
        return value_chain

    def isOpen(self):
        return self.ser.isOpen()

    def dummyMode(self):
        return self.dummyPlug
