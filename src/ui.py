import sys, os, photo, photolib
from PyQt6.QtWidgets import (
    QApplication, 
    QLabel,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QScrollArea
)



class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Photo Library Tools")
        

        self.navStack = QStackedWidget()


        self.pathForm = QFormLayout()
        self.pathInput = QLineEdit()
        self.pathInput.setFixedWidth(400)
        self.pathForm.addRow("Library path:", self.pathInput)
        self.pathSubmitButton = QPushButton("Enter")
        self.pathSubmitButton.clicked.connect(lambda x: self._initPhotoLibrary(self.pathInput.text(), self.startWidg))

        self.startPage = QVBoxLayout()
        self.startPage.addLayout(self.pathForm)
        self.warningMsg = QLabel("Invalid path, try again.")
        self.startPage.addWidget(self.warningMsg)
        self.warningMsg.hide()
        self.startPage.addWidget(self.pathSubmitButton)

        self.startWidg = QWidget()
        self.startWidg.setLayout(self.startPage)

        self.navStack.addWidget(self.startWidg)        
        self.setCentralWidget(self.navStack)
        self.adjustSize()
    



    def _initPhotoLibrary(self, path, prev):
        try:
            self.pl = photolib.PhotoLibrary(path)
            self._buildLibView(prev)
        except FileNotFoundError:
            self.pathInput.setText("")
            self.warningMsg.show()



    
    def _buildLibView(self, prev):
        self.libName = QLabel(os.path.basename(self.pl.path))
        self.scrollList = QScrollArea()
        self.libAsStringBox = QVBoxLayout()
        for line in str(self.pl).split('\n'):
            newLabel = QLabel(line)
            self.libAsStringBox.addWidget(newLabel)
        self.scrollWidg = QWidget()
        self.scrollWidg.setLayout(self.libAsStringBox)
        self.scrollList.setWidget(self.scrollWidg)
        


        self.buttonGroup = QHBoxLayout()
        self.folderButton = QPushButton("Separate to folders")
        self.folderButton.clicked.connect(lambda x: self._updateContents(self.pl.separateImagesToFolders, self.mainLibWidg))
        self.ungroupButton = QPushButton("Ungroup to root")
        self.ungroupButton.clicked.connect(lambda x: self._updateContents(self.pl.ungroupAll, self.mainLibWidg))
        self.buttonGroup.addWidget(self.folderButton)
        self.buttonGroup.addWidget(self.ungroupButton)

        self.mainLibScreen = QVBoxLayout()
        self.mainLibScreen.addWidget(self.libName)
        self.mainLibScreen.addWidget(self.scrollList)
        self.mainLibScreen.addLayout(self.buttonGroup)

        self.mainLibWidg = QWidget()
        self.mainLibWidg.setLayout(self.mainLibScreen)
        self.navStack.addWidget(self.mainLibWidg)
        self.navStack.removeWidget(prev)
        self.adjustSize()
    

    def _updateContents(self, func, prev):
        func()
        self._buildLibView(prev)
    




if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())