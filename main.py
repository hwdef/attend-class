import os
import sqlite3

from view.view import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import sys


class ui_view(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ui_view, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        super().setupUi(MainWindow)
        self.import_information_button.clicked.connect(self.choose_dir)
        self.clear_information_button.clicked.connect(self.delete_data)

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

    def delete_data(self):
        reply = QMessageBox.question(self, '确认', '确定要清除数据吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.system('rm data.db')

def view_show():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_view()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    view_show()
