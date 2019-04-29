
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QLabel, QPushButton, QWidget,
                             QStackedLayout, QListWidget,
                             QVBoxLayout, QStackedWidget,
                             QGridLayout)
from PyQt5.QtCore import QRect, Qt

class Ui(QWidget):

    def setupUi(self, Main):

        Main.setObjectName("Main")
        Main.setFixedSize(900, 500)

        self.width = 900
        self.height = 500

        self.setFixedSize(self.width, self.height)

        '''MENU ON THE MAIN WINDOW'''
        self.menu = QStackedLayout()

        self.mainMenu = QWidget()
        self.howToMenu = QWidget()

        self.mainMenuUi()
        self.howToMenuUi()

        self.menu.addWidget(self.mainMenu)
        self.menu.addWidget(self.howToMenu)

        '''MENU ON THE HOWTO WINDOW'''        
        #self.howToMenuMenu = QStackedLayout()

        #self.howToOverView    = QWidget()
        #self.howToLevel       = QWidget()
        #self.howToTapeMeasure = QWidget()
        #self.howToTheodolite  = QWidget()

        #self.   overViewUi()
        #self.      levelUi()
        #self.tapeMeasureUi()
        #self. theodoliteUi()

        #self.howToMenuMenu.addWidget(self.howToOverView   )
        #self.howToMenuMenu.addWidget(self.howToLevel      )
        #self.howToMenuMenu.addWidget(self.howToTapeMeasure)
        #self.howToMenuMenu.addWidget(self.howToTheodolite )

    def mainMenuUi(self):

        self.mainMenu.setFixedSize(self.width, self.height)

        self.mainMenuText = QLabel(self.mainMenu)
        self.mainMenuText.setGeometry(QRect(30, 120, 480, 200))
        self.mainMenuText.setStyleSheet("font: 14pt Century Gothic")
        self.mainMenuText.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.mainMenuText.setText("Welcome to the Surveying Traverse Calculator!")

        self.howToButton = QPushButton("HOW TO DO A TRAVERSE", self.mainMenu)

        self.howToButton.setGeometry(140, 180, 200, 30)

    def howToMenuUi(self):
        
        self.howToMenu_layout = QGridLayout()

        self.howToMenu.setFixedSize(self.width, self.height)

        self.menuButton1 = QPushButton("Back to main menu")
        self.menuButton1.setGeometry(QRect(10, 10, 200, 30))

        self.howToTitle = QLabel()
        self.howToTitle.setGeometry(QRect(10, 50, self.width, 40))
        self.howToTitle.setStyleSheet("font: 14pt Century Gothic")
        self.howToTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.howToTitle.setText("How to Do a Traverse")

        self.howToSteps = QListWidget()
        self.howToSteps.setGeometry(QRect(10, 100, 200, 80))
        self.howToSteps.insertItem(0, "OVERVIEW"    )
        self.howToSteps.insertItem(1, "LEVEL"       )
        self.howToSteps.insertItem(2, "TAPE MEASURE")
        self.howToSteps.insertItem(3, "THEODOLITE"  )
        self.howToSteps.currentRowChanged.connect(self.display_traverse)

        self.overview_container = QWidget()
        self.level_container = QWidget()
        self.tape_measure_container = QWidget()
        self.theodolite_container = QWidget()
        
        self.overViewUi()
        self.levelUi()
        self.tapeMeasureUi()
        self.theodoliteUi()

        self.traverse_action = QStackedWidget()
        self.traverse_action.addWidget(self.overview_container) 
        self.traverse_action.addWidget(self.level_container) 
        self.traverse_action.addWidget(self.tape_measure_container) 
        self.traverse_action.addWidget(self.theodolite_container) 
        self.traverse_action.setCurrentIndex(0)

        self.howToMenu_left_layout = QVBoxLayout()
        self.howToMenu_left_layout.addWidget(self.menuButton1)
        self.howToMenu_left_layout.addWidget(self.howToTitle)
        self.howToMenu_left_layout.addWidget(self.howToSteps)

        self.howToMenu_layout.addLayout(self.howToMenu_left_layout,0,0,1,1)
        self.howToMenu_layout.addWidget(self.traverse_action,0,1,1,1)
        self.howToMenu.setLayout(self.howToMenu_layout)

    def overViewUi(self):
        self.overview_layout = QVBoxLayout()
        self.overview_button = QPushButton('Overview')
        self.overview_layout.addWidget(self.overview_button)
        self.overview_container.setLayout(self.overview_layout)

    def levelUi(self):
        self.level_layout = QVBoxLayout()
        self.level_button = QPushButton('Level')
        self.level_layout.addWidget(self.level_button)
        self.level_container.setLayout(self.level_layout)

    def tapeMeasureUi(self):
        self.tape_measure_layout = QVBoxLayout()
        self.tape_measure_button = QPushButton('Tape measure')
        self.tape_measure_layout.addWidget(self.tape_measure_button)
        self.tape_measure_container.setLayout(self.tape_measure_layout)

    def theodoliteUi(self):
        self.theodolite_layout = QVBoxLayout()
        self.theodolite_button = QPushButton('Theodolite')
        self.theodolite_layout.addWidget(self.theodolite_button)
        self.theodolite_container.setLayout(self.theodolite_layout)

    def display_traverse(self, index):
        self.traverse_action.setCurrentIndex(index)

class Main(QMainWindow, Ui):

    def __init__(self):

        super(Main, self).__init__()

        self.setupUi(self)

        self.menuButton1.clicked.connect(self.menuWindow)
        self.howToButton.clicked.connect(self.howToWindow)

    def menuWindow(self):

        self.menu.setCurrentIndex(0)

    def howToWindow(self):

        self.menu.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = Main()
    sys.exit(app.exec())
