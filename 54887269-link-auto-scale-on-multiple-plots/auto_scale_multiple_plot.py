import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys
import random

class AutoScaleMultiplePlotWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AutoScaleMultiplePlotWidget, self).__init__(parent)

        self.NUMBER_OF_PLOTS = 4
        self.LEFT_X = 0 
        self.RIGHT_X = 5
        self.SPACING = 1
        self.x_axis = np.arange(self.LEFT_X, self.RIGHT_X + 1, self.SPACING)
        self.buffer_size = int((abs(self.LEFT_X) + abs(self.RIGHT_X) + 1)/self.SPACING)

        self.auto_scale_plot_widget = pg.PlotWidget()
        self.auto_scale_plot_widget.setLabel('left', 'left axis')

        # Create plots
        self.left_plot1 = self.auto_scale_plot_widget.plot()
        self.left_plot2 = self.auto_scale_plot_widget.plot()
        self.left_plot3 = self.auto_scale_plot_widget.plot()
        self.left_plot4 = self.auto_scale_plot_widget.plot()

        self.left_plot1.setPen((173,255,129), width=1)
        self.left_plot2.setPen((172,187,255), width=1)
        self.left_plot3.setPen((255,190,116), width=1)
        self.left_plot4.setPen((204,120,255), width=1)

        self.initialize_plot_buffers()
        self.initialize_data_buffers()

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.auto_scale_plot_widget)

        self.start()

    def initialize_data_buffers(self):
        """Create blank data buffers for each curve"""

        self.data_buffers = []
        for trace in range(self.NUMBER_OF_PLOTS):
            self.data_buffers.append([0])

    def initialize_plot_buffers(self):
        """Add plots into buffer for each curve"""

        self.plots = []
        self.plots.append(self.left_plot1)
        self.plots.append(self.left_plot2)
        self.plots.append(self.left_plot3)
        self.plots.append(self.left_plot4)

    def update_plot(self):
        """Generates new random value and plots curve onto plot"""

        for trace in range(self.NUMBER_OF_PLOTS):
            if len(self.data_buffers[trace]) >= self.buffer_size:
                self.data_buffers[trace].pop(0)
            data_point = self.data_buffers[trace][-1] + random.randint(10,50)
            self.data_buffers[trace].append(float(data_point))

            self.plots[trace].setData(self.x_axis[len(self.x_axis) - len(self.data_buffers[trace]):], self.data_buffers[trace])

    def get_auto_scale_plot_layout(self):
        return self.layout

    def start(self):
        self.multiple_axis_plot_timer = QtCore.QTimer()
        self.multiple_axis_plot_timer.timeout.connect(self.update_plot)
        self.multiple_axis_plot_timer.start(500)

if __name__ == '__main__':

    # Create main application window
    app = QtGui.QApplication([])
    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Auto Scale Multiple Plot Example')

    # Create plot
    auto_scale_plot = AutoScaleMultiplePlotWidget()

    # Create and set widget layout
    # Main widget container
    cw = QtGui.QWidget()
    ml = QtGui.QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)

    # Add plot to main layout
    ml.addLayout(auto_scale_plot.get_auto_scale_plot_layout(),0,0)

    mw.show()

    if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
