from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import sys
from random import randint
import numpy as np
import math

from communicate import Communication

class MyWindow(pg.GraphicsWindow):
    def __init__(self, serial):
        super(MyWindow, self).__init__()
        xpos = 200
        ypos = 200
        self.width = 1200
        height = 700
        self.setGeometry(xpos, ypos, self.width, height)
        self.setWindowTitle('Ground Station')
        self.serial = serial
        
        # self.view = pg.GraphicsView()
        self.Layout = pg.GraphicsLayout()
        self.setCentralItem(self.Layout)

        self.initUI()

    def initUI(self):
        text = """Мониторинг полета кансат. <br>
                        Команда: Чолбон"""
        self.Layout.addLabel(text,fontSize=25)
        self.Layout.nextRow()

        # Acceleration graph
        l1 = self.Layout.addLayout(colspan=20,rowspan=1)
        l11 = l1.addLayout(rowspan=1, border=(83, 83, 83))
        acc_graph = l11.addPlot(title="Accelerations (m/s²)") 
        acc_graph.addLegend()
        self.accX_plot = acc_graph.plot(pen=(102, 252, 241), name="X")
        self.accY_plot = acc_graph.plot(pen=(29, 185, 84), name="Y")
        self.accZ_plot = acc_graph.plot(pen=(203, 45, 111), name="Z")
        self.accX_data = np.linspace(0, 0)
        self.accY_data = np.linspace(0, 0)
        self.accZ_data = np.linspace(0, 0)
        self.ptr1 = 0

        # Velocity graph
        
        l12 = l1.addLayout(rowspan=1, border=(83, 83, 83))
        graph_vel = l12.addPlot(title="Speed (m/s)")
        self.vel_plot = graph_vel.plot(pen=(29, 185, 84))
        self.vel_data = np.linspace(0, 0, 30)
        self.ptr3 = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.vel = 0

        self.Layout.nextRow()

        # Temperature graph
        l2 = self.Layout.addLayout(colspan=20,rowspan=2)
        l21 = l2.addLayout(rowspan=1, border=(83, 83, 83))
        graf_temp = l21.addPlot(title="Temperature (ºc)")
        self.temp_plot = graf_temp.plot(pen=(29, 185, 84))
        self.temp_data = np.linspace(0, 0, 30)
        self.ptr2 = 0

       

        

    def update_vel(self,data):
        i = 0
        if(i == 0):
            vzo = float(data[10])
            i += 1

        self.vx += (float(data[8])) * 500
        self.vy += (float(data[9])) * 500
        self.vz += (float(data[10]) - vzo) * 500
        sum = math.pow(self.vx, 2) + math.pow(self.vy, 2) + math.pow(self.vz, 2)
        self.vel = math.sqrt(sum)
        self.vel_data[:-1] = self.vel_data[1:]
        self.vel_data[-1] = self.vel
        self.ptr3 += 1
        self.vel_plot.setData(self.vel_data)
        self.vel_plot.setPos(self.ptr3, 0)

    def update_temp(self,data):
        self.temp_data[:-1] = self.temp_data[1:]
        self.temp_data[-1] = float(data[3])
        self.ptr2 += 1
        self.temp_plot.setData(self.temp_data)
        self.temp_plot.setPos(self.ptr2, 0)
    
    def update_acc(self,data):
        self.accX_data[:-1] = self.accX_data[1:]
        self.accY_data[:-1] = self.accY_data[1:]
        self.accZ_data[:-1] = self.accZ_data[1:]

        self.accX_data[-1] = float(data[8])
        self.accY_data[-1] = float(data[9])
        self.accZ_data[-1] = float(data[10])
        self.ptr2 += 1

        self.accX_plot.setData(self.accX_data)
        self.accY_plot.setData(self.accY_data)
        self.accZ_plot.setData(self.accZ_data)

        self.accX_plot.setPos(self.ptr2, 0)
        self.accY_plot.setPos(self.ptr2, 0)
        self.accZ_plot.setPos(self.ptr2, 0)
    def update(self):
        data = self.serial.getData()
        self.update_acc(data)
        self.update_temp(data)
        self.update_vel(data)

def window():
    app = QApplication(sys.argv)
    serial = Communication()
    win = MyWindow(serial)

    if(serial.isOpen()) or (serial.dummyMode()):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(win.update)
        timer.start(500)
    else:
        print("something is wrong with the update call")
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()