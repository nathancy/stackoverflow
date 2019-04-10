from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Rectangle3D(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Elevated 3D rectangle color settings
        self.elevated_border_color = QtGui.QColor(111,211,111)
        self.elevated_fill_color = QtGui.QColor(0,255,0)
        self.elevated_pen_width = 3

        # Lowered 3D rectangle color settings
        self.lowered_border_color = QtGui.QColor(0,235,0)
        self.lowered_fill_color = QtGui.QColor(0,178,0)
        self.lowered_pen_width = 3

    def draw3DRectangle(self, x, y, w, h, raised=True):
        # Specify the border/fill colors depending on raised or lowered
        if raised:
            # Line color (border)
            self.pen = QtGui.QPen(self.elevated_border_color, self.elevated_pen_width)
            # Fill color
            self.fill = QtGui.QBrush(self.elevated_fill_color)
        else:
            # Line color (border)
            self.pen = QtGui.QPen(self.lowered_border_color, self.lowered_pen_width)
            # Fill color
            self.fill = QtGui.QBrush(self.lowered_fill_color)

        painter = QtGui.QPainter(self)

        # Draw border color of rectangle
        painter.setPen(self.pen)
        painter.setBrush(self.fill)  
        painter.drawRect(x, y, w, h)

        # Cover up the top and left sides with filled color using lines
        if raised:
            painter.setPen(QtGui.QPen(self.elevated_fill_color, self.elevated_pen_width))
        else:
            painter.setPen(QtGui.QPen(self.lowered_fill_color, self.lowered_pen_width))

        painter.drawLine(x, y, x + w, y) 
        painter.drawLine(x, y, x, y + h)

    def paintEvent(self, event):
        self.draw3DRectangle(50,50,300,150,True)
        self.draw3DRectangle(50,250,300,150,False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 

    widget = Rectangle3D()
    widget.show()

    sys.exit(app.exec_())
