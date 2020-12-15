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


def asc(ui,sqlCommand):
    q = QSqlQuery()
    q.prepare(sqlCommand)
    # q.prepare('insert into buff1 (id,name) value(1,"shit")')
    print("执行一次asc():sql语句为:"+sqlCommand)
    q.exec()
    model = QSqlQueryModel()
    model.setQuery(q)
    #设置表头
    modelDic = ['id','物品名','挂刀比例','倒货收益率','倒货收益','steam底价',
               'buff底价','buff在售数','buff求购数','buff求购价','磨损','品类','物品种类','steam商城链接','上次更新时间']
    for i in range(0,14):
        model.setHeaderData(i, Qt.Orientation(1),modelDic[i])
    ui.tableView.setModel(model)

def pushButtonSlot(ui):
    print("?")
    asc(ui,'久经沙场')


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
    asc(ui,'崭新出厂')
    sys.exit(app.exec_())


