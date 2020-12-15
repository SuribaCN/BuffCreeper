import sys
import untitled    # 注意，此模块名称为编译生成的 PyQT Python文件
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtSql
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlQueryModel
from getDetils import *


def asc():
    q = QSqlQuery()
    q.prepare("select * from buff where exterior like '崭新出厂' order by scale_buff2steam ASC limit 100")
    # q.prepare('insert into buff1 (id,name) value(1,"shit")')
    print(q.value(3))
    q.exec()
    model = QSqlQueryModel()
    model.setQuery(q)
    modelDic = ['id','物品名','挂刀比例','倒货收益率','倒货收益','steam底价',
               'buff底价','buff在售数','buff求购数','buff求购价','磨损','种类','steam商城链接','上次更新时间']
    for i in range(0,13):
        model.setHeaderData(i, Qt.Orientation(1),modelDic[i])
    ui.tableView.setModel(model)

def pushButtonSlot():
    asc()


if __name__ == '__main__':
    #连接数据库
    database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    database.setDatabaseName('database.db')
    database.open()
    #启动主页面
    # urlAnalyze('smg')
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = untitled.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    asc()
    sys.exit(app.exec_())


