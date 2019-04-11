from matplotlib.figure import Figure
from matplotlib import animation
import numpy as np
import sys, matplotlib
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QHBoxLayout(self._main)
        
        # Configure figure 1 
        self.fig1 = Figure(figsize=(5, 3))
        self.canvas1 = FigureCanvas(self.fig1)

        # Configure figure 2
        self.fig2 = Figure(figsize=(5, 3))
        self.canvas2 = FigureCanvas(self.fig2)

        layout.addWidget(self.canvas1)
        layout.addWidget(self.canvas2)
        self.addToolBar(NavigationToolbar(self.canvas1, self))
        self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.canvas2, self))

        self.setup()

    def setup(self):
        # Plot 1 (top)
        self.ax1 = self.fig1.subplots()
        self.ax1.set_aspect('equal')
        self.ax1.grid(True, linestyle = '-', color = '0.10')
        self.ax1.set_xlim([-15, 15])
        self.ax1.set_ylim([-15, 15])
        
        # Plot 2 (bottom)
        self.ax2 = self.fig2.subplots()
        self.ax2.set_aspect('equal')
        self.ax2.grid(True, linestyle = '-', color = '0.10')
        self.ax2.set_xlim([-15, 15])
        self.ax2.set_ylim([-15, 15])

        self.scat1 = self.ax1.scatter([], [], c=(0.9, 0.1, 0.5),  zorder=3)
        self.scat1.set_alpha(0.8)

        self.scat2 = self.ax2.scatter([], [], c=(0.9, 0.1, 0.5),  zorder=3)
        self.scat2.set_alpha(0.8)

        self.anim1 = animation.FuncAnimation(self.fig1, self.update1,frames = 720, interval = 10)
        self.anim2 = animation.FuncAnimation(self.fig2, self.update2,frames = 720, interval = 10)
    
    # Update data for plot 1
    def update1(self, i):
        self.scat1.set_offsets(([np.cos(np.radians(i))*7.5, np.sin(np.radians(i))*7.5], [0,0]))

    # Update data for plot 2
    def update2(self, i):
        self.scat2.set_offsets(([np.cos(np.radians(i))*7.5, np.sin(np.radians(i))*7.5], [0,0]))

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
