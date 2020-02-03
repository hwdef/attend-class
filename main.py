import os
import sqlite3

from view.view import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import sys

class ui_main(QMainWindow, Ui_MainWindow):
    # def __init__(self, parent=None):
    #     super(ui_main, self).__init__(parent)
    #     # self.setupUi(self)

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        super().setupUi(MainWindow)
        self.import_information_button.clicked.connect(self.choose_dir)
        self.clear_information_button.clicked.connect(self.delete_data)
        self.comboBox.addItem('')
        if os.path.exists('data.db'):
            self.add_comboBox()

    def add_comboBox(self):
        class_data = self.get_class()
        self.comboBox.addItems(class_data)
        self.comboBox.currentTextChanged.connect(self.choose_class)

    def get_class(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT DISTINCT class FROM information")
        class_data = []
        for row in cursor:
            class_data.append(row[0])
        conn.close()
        return class_data

    def choose_class(self):
        choosed_class = self.comboBox.currentText()
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        cursor = c.execute("SELECT id,name FROM information WHERE class=?",(choosed_class,))
        for row in cursor:
            student = row[1]+row[0]
            self.checkBox = QtWidgets.QCheckBox(self.name_list)
            self.checkBox.setObjectName("checkBox")
            self.checkBox.setText(student)
            self.verticalLayout.addWidget(self.checkBox)
            self.checkBox = QtWidgets.QCheckBox(self.name_list)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

    def choose_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        if directory != '':
            data = []
            files_name = os.listdir(directory)
            for file_name in files_name:
                file_name_split = file_name.split(',')
                file_name_split.append('')
                data.append(file_name_split)
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE information
                    (
                        id text,
                        name text,
                        class text,
                        check_in text
                    );''')
            c.executemany("INSERT INTO information VALUES (?,?,?,?)", data)
            conn.commit()
            conn.close()
            self.add_comboBox()

    def delete_data(self):
        reply = QMessageBox.question(self, '确认', '确定要清除数据吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.system('rm data.db')

def view_show():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    view_show()
