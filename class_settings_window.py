from PyQt4.QtGui import *
from PyQt4.QtCore import *
from settings import settings_dict
import os

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Settings')
        self.setGeometry(600, 150, 400, 300)
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.label_path = QLabel('Folder to store images:')
        self.new_path = QLineEdit()
        self.new_path.setReadOnly(True)
        self.new_path.setText(settings_dict['output_path'])
        self.browse_button = QPushButton('Browse folder')
        self.browse_button.clicked.connect(self.click_browse)
        self.save_changes_button = QPushButton('Save Changes')
        self.save_changes_button.clicked.connect(self.click_save_changes)

        self.settings_grid = QGridLayout()
        self.settings_grid.addWidget(self.label_path, 0, 0)
        self.settings_grid.addWidget(self.browse_button,0,1)
        self.settings_grid.addWidget(self.new_path, 1, 0)
        self.settings_grid.addWidget(self.save_changes_button, 2, 0)
        self.setLayout(self.settings_grid)

    def click_save_changes(self):
        with open("settings.py", "w") as f:
            f.write("settings_dict = {{\'output_path\':\'{0}\',\'move\':1}}".format(self.new_path.text()))
            f.close()
    def click_browse(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder to store images...')
        self.new_path.setText(folder_path.replace('\\','/'))