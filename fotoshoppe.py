import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor, QPixmap
from PIL import Image, ImageOps

my_filters = ["Pick a filter", "Sepia", "Negative", "Grayscale", "Thumbnail", "None"]


class SaveWindow(QWidget):
    def __init__(self, im):
        super().__init__()
        self.filtered = im
        self.save_image = QPushButton("Save")
        hbox = QHBoxLayout()
        hbox.addWidget(self.save_image)
        mbox = QVBoxLayout()
        mbox.addLayout(hbox)
        self.setLayout(mbox)

        self.save_image.clicked.connect(self.save_new)

    @pyqtSlot()
    def save_new(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            self.filtered.save(fileName, 'PNG')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.insert_file = QPushButton("Insert File")
        hbox = QHBoxLayout()
        hbox.addWidget(self.insert_file)

        self.combo_box = QComboBox()
        self.combo_box.addItems(my_filters)
        self.submit = QPushButton('Submit')
        self.line1 = QLineEdit("<Input a file>")
        vbox = QVBoxLayout()
        vbox.addWidget(self.line1)
        vbox.addWidget(self.combo_box)
        vbox.addWidget(self.submit)

        mbox = QVBoxLayout()
        mbox.addLayout(hbox)
        mbox.addLayout(vbox)

        self.setLayout(mbox)
        self.insert_file.clicked.connect(self.get_file)
        self.submit.clicked.connect(self.new_win)
        self.setWindowTitle("Image Search")

    @pyqtSlot()
    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.line1.setText(fileName)

    def new_win(self):
        my_filter = self.combo_box.currentText()
        pathway = self.line1.text()
        print(str(pathway))
        im = Image.open(pathway)

        #Once an image is chosen with chooser, we will apply
        #a filter to it.

        if (my_filter == "Sepia"):
            new_list = []
            for p in im.getdata():
                temp = (p[0], int(p[1]*.7), int(p[2]*.7))
                new_list.append(temp)
            im.putdata(new_list)
            # im.save('images/sepia.jpg')
            # newIM = Image.open('images/sepia.jpg')
            self.save_pic = SaveWindow(im)
            im.show()
            self.save_pic.show()
        if (my_filter == "Negative"):
            newIm = ImageOps.invert(im)
            self.save_pic = SaveWindow(newIm)
            newIm.show()
            self.save_pic.show()
        elif (my_filter == "Grayscale"):
            newIm = im.convert('LA')
            self.save_pic = SaveWindow(newIm)
            newIm.show()
            self.save_pic.show()
        elif (my_filter == "Thumbnail"):
            size = (128, 128)
            im.thumbnail(size)
            im.save('images/thumbnail.jpg')
            newIM = Image.open('images/thumbnail.jpg')
            newIM.show()
        elif (my_filter == "None"):
            im.show()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
