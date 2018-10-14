from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sqlite3 as lite
from PIL import Image
import sys
import os
from PIL import Image
from class_read_tags import *
import time
import datetime
from shutil import copyfile

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(400, 200, 450, 500)
        self.setWindowTitle('Image Management Tool')

        #==========Main Menu====================
        self.newGame = QAction('&New Game', self)
        self.statusBar()
        self.mainMenu = self.menuBar()
        optionsMenu = self.mainMenu.addMenu('&Options')
        optionsMenu.addAction(self.newGame)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)




class MyTableWidget(QWidget):
    images_list = []

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Add New Image")
        self.tabs.addTab(self.tab2, "Search For Image")

        conn = lite.connect('database.db')
        cur = conn.cursor()

        #===============FIRST TAB (Add new file)=================================


        self.tab1_browse_button = QPushButton("Browse Folder")
        self.tab1_browse_button.clicked.connect(self.click_browse_folder)

        self.tab1_next_button = QPushButton("Next >>")
        self.tab1_next_button.clicked.connect(self.click_next)
        self.tab1_previous_button = QPushButton("<< Prev")
        self.tab1_previous_button.clicked.connect(self.click_previous)
        self.tab1_store_this_image = QPushButton("Store this image")
        self.tab1_store_this_image.clicked.connect(lambda: self.click_store_image(cur,conn))


        self.tab1_display_image = QLabel()
        self.tab1_text1 = QLabel('Image name:')
        self.tab1_display_name = QLineEdit()
        self.tab1_text2 = QLabel('Image path:')
        self.tab1_display_path = QLineEdit()
        self.tab1_text3 = QLabel('Provide tags (if any field filled, image already have):')
        self.tab1_tag1 = QLineEdit()
        self.tab1_tag2 = QLineEdit()
        self.tab1_tag3 = QLineEdit()
        self.tab1_tag4 = QLineEdit()

        #Grids

        self.tab1_left_grid = QGridLayout()
        self.tab1_left_upper_grid = QGridLayout()
        self.tab1_right_grid = QGridLayout()
        self.tab1_main_grid = QGridLayout()

        #Add widgets and layouts
        self.tab1_left_upper_grid.addWidget(self.tab1_previous_button,0,0)
        self.tab1_left_upper_grid.addWidget(self.tab1_next_button, 0, 1)


        self.tab1_left_grid.addLayout(self.tab1_left_upper_grid,0,0)
        self.tab1_left_grid.addWidget(self.tab1_display_image,1,0)
        self.tab1_left_grid.addWidget(self.tab1_browse_button,2,0)

        self.tab1_right_grid.addWidget(self.tab1_text1,0,0)
        self.tab1_right_grid.addWidget(self.tab1_store_this_image, 0, 1)
        self.tab1_right_grid.addWidget(self.tab1_display_name, 1, 0)
        self.tab1_right_grid.addWidget(self.tab1_text2, 3, 0)
        self.tab1_right_grid.addWidget(self.tab1_display_path, 4, 0)
        self.tab1_right_grid.addWidget(self.tab1_text3,5 ,0)
        self.tab1_right_grid.addWidget(self.tab1_tag1, 6, 0)
        self.tab1_right_grid.addWidget(self.tab1_tag2, 6, 1)
        self.tab1_right_grid.addWidget(self.tab1_tag3, 7, 0)
        self.tab1_right_grid.addWidget(self.tab1_tag4, 7, 1)

        self.tab1_main_grid.addLayout(self.tab1_left_grid,0,0)
        self.tab1_main_grid.addLayout(self.tab1_right_grid,0,1)
        self.tab1.setLayout(self.tab1_main_grid)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    @classmethod
    def images_list_append(cls, value):
        cls.images_list.append(value)


    def click_store_image(self,cur,conn):
        if self.tab1_display_image.pixmap() == None:
            return 0
        #File_Name TEXT, File_Path TEXT, Previous_Path TEXT,Tag1 TEXT,Tag2 TEXT, Tag3 TEXT, Tag4 TEXT, Date_added TEXT,
        file_name = self.tab1_display_name.text()[:-4]
        date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        cur.execute("INSERT INTO images (File_Name, Previous_Path,Tag1,Tag2,Tag3,Tag4,Date_added) VALUES (?,?,?,?,?,?,?)",
                    (file_name,self.tab1_display_path.text(),self.tab1_tag1.text(),
                     self.tab1_tag2.text(),self.tab1_tag3.text(),self.tab1_tag4.text(),date,))
        conn.commit()
        copyfile(os.path.join(self.tab1_display_path.text(), self.tab1_display_name.text()),os.path.join('images',self.tab1_display_name.text()))

    def click_browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select folder with images...')

        for dirpath, dirnames, filenames in os.walk(folder_path):
            for fn in filenames:
                if fn.endswith('.jpg'):     #initial check if the file is jpeg
                    img = Image.open(os.path.join(folder_path, fn))
                    if img.format == 'JPEG':        #Pillow check for jpeg files

                        self.images_list_append(fn)     #append to the images list

        #update application labels and fields
        self.pixmap = QPixmap(folder_path + '/' + self.images_list[0])
        self.pixmap = self.pixmap.scaledToWidth(360)

        self.tab1_display_image.setPixmap(self.pixmap)
        self.tab1_display_path.setText(folder_path)
        self.tab1_display_name.setText(self.images_list[0])
        #update tags
        tags = ReadTags(str(os.path.join(folder_path, self.tab1_display_name.text())))
        tab1_tag_list = [self.tab1_tag1,self.tab1_tag2,self.tab1_tag3,self.tab1_tag4]
        for elem in tab1_tag_list:
            elem.setText('')
        for counter, tag in enumerate(tags.tags):
            tab1_tag_list[counter].setText(tag)


    def click_next(self):
        if self.tab1_display_name.text() == '' or self.tab1_display_name.text() not in self.images_list:
            return 0
        index = self.images_list.index(self.tab1_display_name.text())
        if index + 1 == len(self.images_list):
            index = 0
        else:
            index = index + 1
        print(index)
        self.pixmap = QPixmap(self.tab1_display_path.text() + '/' + self.images_list[index])
        self.pixmap = self.pixmap.scaledToWidth(360)
        self.tab1_display_image.setPixmap(self.pixmap)
        self.tab1_display_name.setText(self.images_list[index])
        #tags
        tags = ReadTags(str(os.path.join(self.tab1_display_path.text(), self.tab1_display_name.text())))
        tab1_tag_list = [self.tab1_tag1, self.tab1_tag2, self.tab1_tag3, self.tab1_tag4]
        for elem in tab1_tag_list:
            elem.setText('')
        for counter, tag in enumerate(tags.tags):
            tab1_tag_list[counter].setText(tag)

    def click_previous(self):
        if self.tab1_display_name.text() == '' or self.tab1_display_name.text() not in self.images_list:
            return 0
        index = self.images_list.index(self.tab1_display_name.text())
        if index - 1 < 0:
            index = len(self.images_list) - 1
        else:
            index = index - 1

        self.pixmap = QPixmap(self.tab1_display_path.text() + '/' + self.images_list[index])
        self.pixmap = self.pixmap.scaledToWidth(360)
        self.tab1_display_image.setPixmap(self.pixmap)
        self.tab1_display_name.setText(self.images_list[index])
        # tags
        tags = ReadTags(str(os.path.join(self.tab1_display_path.text(), self.tab1_display_name.text())))
        tab1_tag_list = [self.tab1_tag1, self.tab1_tag2, self.tab1_tag3, self.tab1_tag4]
        for elem in tab1_tag_list:
            elem.setText('')
        for counter, tag in enumerate(tags.tags):
            tab1_tag_list[counter].setText(tag)

def main():
    conn = lite.connect('database.db')
    cur = conn.cursor()
    create_table(cur)

    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    window.raise_()

    sys.exit(app.exec_())
    conn.close()
    cur.close()

def create_table(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS Images(Id INTEGER PRIMARY KEY AUTOINCREMENT, File_Name TEXT, File_Path TEXT, Previous_Path TEXT,Tag1 TEXT,Tag2 TEXT, Tag3 TEXT, Tag4 TEXT, Date_added TEXT)")


if __name__ == '__main__':
    main()