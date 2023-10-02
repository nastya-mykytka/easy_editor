import os
from pathlib import Path

from PIL import Image
from PIL.ImageFilter import SHARPEN
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QListWidgetItem
)

app = QApplication([])
app.setStyleSheet(Path('app.css').read_text())

window = QWidget()

window.setWindowTitle("Розумні замітки")
width = 1200
height = 800
window.resize(width, height)
window.show()

main_layout = QHBoxLayout()

file_layout = QHBoxLayout()
picture_layout = QHBoxLayout()
left_Layout = QVBoxLayout()
right_Layout = QVBoxLayout()
folder_Layout = QVBoxLayout()
control_buttons_layout = QHBoxLayout()

folder_button = QPushButton('Папка')

image_view = QLabel('Тут буде твоє зображення')
left_button = QPushButton('Ліворуч')
right_button = QPushButton('Праворуч')
mirror_button = QPushButton('Дзеркало')
contrast_button = QPushButton('Різкізть')
black_white_button = QPushButton('Ч\Б')

folder_Layout.addWidget(folder_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

picture_layout.addWidget(image_view)

control_buttons_layout.addWidget(left_button)
control_buttons_layout.addWidget(right_button)
control_buttons_layout.addWidget(mirror_button)
control_buttons_layout.addWidget(contrast_button)
control_buttons_layout.addWidget(black_white_button)

left_Layout.addLayout(folder_Layout)
left_Layout.addLayout(file_layout)

right_Layout.addLayout(picture_layout, stretch=1)
right_Layout.addLayout(control_buttons_layout)

main_layout.addLayout(left_Layout)
main_layout.addLayout(right_Layout)

main_layout.addWidget(folder_button)

window.setLayout(main_layout)

lb_image = QLabel('Тут буде картинка')

workdir = ''
image_list = QListWidget()


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    image_list.clear()
    for filename in filenames:
        image_list.addItem(QListWidgetItem(filename))
    file_layout.addWidget(image_list)


folder_button.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def showImage(self, path):
        image_view.hide()
        pixmapimage = QPixmap(path)
        w, h = image_view.width(), image_view.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image_view.setPixmap(pixmapimage)
        image_view.show()

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_black_white(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


workimage = ImageProcessor()


def showChosenImage():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


image_list.currentRowChanged.connect(showChosenImage)
left_button.clicked.connect(workimage.do_left)
right_button.clicked.connect(workimage.do_right)
mirror_button.clicked.connect(workimage.do_flip)
contrast_button.clicked.connect(workimage.do_sharpen)
black_white_button.clicked.connect(workimage.do_black_white)

app.exec()
