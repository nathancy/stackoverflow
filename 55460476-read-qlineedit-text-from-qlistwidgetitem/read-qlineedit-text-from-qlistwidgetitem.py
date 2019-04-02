
import sys
from PyQt4 import QtGui, QtCore

def Add_OtherItem():
    ItemOther = CustomItem()
    ItemOther.SetupItem(OthersCommandsWidget)

def ReadText_fn():
    for index in range(0,OthersCommandsWidget.count()):

        TargetItem = OthersCommandsWidget.itemWidget(OthersCommandsWidget.item(index)).children()[1].text()
        print(TargetItem)

app = QtGui.QApplication(sys.argv)

class CustomItem(object):

    def SetupItem(self, OthersCommandList):

        self.Item = QtGui.QListWidgetItem()
        self.Item.setStatusTip("TItem")

        self.MainWidget = QtGui.QWidget()

        self.CommandLine = QtGui.QLineEdit("")

        self.DeleteButton = QtGui.QPushButton()
        self.DeleteButton.setFixedSize(22, 22)

        self.ItemLayoutBox = QtGui.QHBoxLayout()

        self.ItemLayoutBox.addWidget(self.CommandLine)
        self.ItemLayoutBox.addWidget(self.DeleteButton)

        self.MainWidget.setLayout(self.ItemLayoutBox)

        self.Item.setSizeHint(self.MainWidget.sizeHint())

        OthersCommandList.addItem(self.Item)
        OthersCommandList.setItemWidget(self.Item, self.MainWidget)

AppWindow = QtGui.QMainWindow()
AppWindow.setWindowTitle("PoC ListWidget")
AppWindow.setFixedSize(550, 550)

TabWindow = QtGui.QTabWidget(AppWindow)
TabWindow.setGeometry(8, 30, 535, 505)

WorkTAB = QtGui.QWidget()
TabWindow.addTab(WorkTAB, 'Tab.01')

OthersCommandsWidget = QtGui.QListWidget(WorkTAB)
OthersCommandsWidget.setGeometry(QtCore.QRect(8, 40, 515, 430))

AddButton = QtGui.QPushButton(WorkTAB)
AddButton.setText("Add Item")
AddButton.setGeometry(QtCore.QRect(8, 8, 0, 0))
AddButton.setFixedSize(70, 22)

AddButton.clicked.connect(Add_OtherItem)

ReadButton = QtGui.QPushButton(WorkTAB)
ReadButton.setText("Read Text")
ReadButton.setGeometry(QtCore.QRect(100, 8, 0, 0))
ReadButton.setFixedSize(70, 22)

ReadButton.clicked.connect(ReadText_fn)

AppWindow.show()
sys.exit(app.exec_())
