from PyQt5 import QtGui  # (the example applies equally well to PySide2)
import pyqtgraph as pg
from communicate import Communication
from numpy import *
import datetime

serial = Communication()

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Signal from serial port") # creates a window
Layout = pg.GraphicsLayout()
Layout.addLabel('test')
win.setCentralItem(Layout)
win.show()

Layout.nextRow()

l1 = Layout.addLayout(colspan=20,rowspan=2)
l11 = l1.addLayout(rowspan=1, border=(83, 83, 83))
p = l11.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
curve = p.plot(pen=(29, 185, 84))                        # create an empty "plot" (a curve to plot)

l2 = Layout.addLayout(colspan=20,rowspan=2)
l21 = l2.addLayout(rowspan=1, border=(83, 83, 83))
p2 = l21.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
curve2 = p.plot(pen=(29, 185, 84))      

windowWidth = 500                       # width of the window displaying the curve
Xm = linspace(0,0,30)          # create array that will contain the relevant time series     
ptr = -windowWidth                      # set first x position

# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global curve, ptr, Xm    
    Xm[:-1] = Xm[1:]                      # shift data in the temporal mean 1 sample left
    value = serial.getData()[1]           # read line (single value) from the serial port
    Xm[-1] = float(value)                 # vector containing the instantaneous values      
    ptr += 1                              # update x position for displaying the curve
    curve.setData(Xm)                     # set the curve with this data
    curve.setPos(ptr,0)                   # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # you MUST process the plot now

### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
if(serial.isOpen()) or (serial.dummyMode()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(500)
else:
    print("something is wrong with the update call")

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################