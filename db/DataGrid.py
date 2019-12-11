import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtSql import *


class DateGrid(QWidget):
    def createTableAndInit(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('./database.db')

        if not self.db.open():
            return False

        query = QSqlQuery()

        query.exec("create table student(id int primary key,name vchar,sex vchar ,age int ,department vchar )")

        query.exec("insert into student values(1,'张三1','男',20,'计算机')")
        query.exec("insert into student values(2,'李四1','男',19,'经管')")
        query.exec("insert into student values(3,'王五1','男',22,'机械')")
        query.exec("insert into student values(4,'赵六1','男',21,'法律')")
        query.exec("insert into student values(5,'小明1','男',20,'英语')")
        query.exec("insert into student values(6,'小李1','女',19,'计算机')")
        query.exec("insert into student values(7,'小张1','男',20,'机械')")
        query.exec("insert into student values(8,'小刚1','男',19,'经管')")
        query.exec("insert into student values(9,'张三2','男',21,'计算机')")
        query.exec("insert into student values(10,'张三3','女',20,'法律')")
        query.exec("insert into student values(11,'王五2','男',19,'经管')")
        query.exec("insert into student values(12,'张三4','男',20,'计算机')")
        query.exec("insert into student values(13,'小李2','男',20,'机械')")
        query.exec("insert into student values(14,'李四2','女',19,'经管')")
        query.exec("insert into student values(15,'赵六3','男',21,'英语')")
        query.exec("insert into student values(16,'李四2','男',19,'法律')")
        query.exec("insert into student values(17,'小张2','女',22,'经管')")
        query.exec("insert into student values(18,'李四3','男',21,'英语')")
        query.exec("insert into student values(19,'小李3','女',19,'法律')")
        query.exec("insert into student values(20,'王五3','女',20,'机械')")
        query.exec("insert into student values(21,'张三4','男',22,'计算机')")
        query.exec("insert into student values(22,'小李2','男',20,'法律')")
        query.exec("insert into student values(23,'张三5','男',19,'经管')")
        query.exec("insert into student values(24,'小张3','女',20,'计算机')")
        query.exec("insert into student values(25,'李四4','男',22,'英语')")
        query.exec("insert into student values(26,'赵六2','男',20,'机械')")
        query.exec("insert into student values(27,'小李3','女',19,'英语')")
        query.exec("insert into student values(28,'王五4','男',21,'经管')")

        return True

    def __init__(self):
        super(DateGrid, self).__init__()
        self.setWindowTitle("分页查询例子")
        self.resize(750, 300)
        self.createTableAndInit()

        self.currentPage = 0
        self.totalPage = 0
        self.totalRecordCount = 0
        self.PageRecordCount = 6
        self.initUI()

    def initUI(self):
        self.createWindow()
        self.setTableView()

        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)

    def closeEvent(self, event):
        self.db.close()

    def createWindow(self):
        operatorLayout = QHBoxLayout()
        self.prevButton = QPushButton("上一页")
        self.nextButton = QPushButton("下一页")
        self.switchPageButton = QPushButton("Go")
        self.switchPageLineEdit = QLineEdit()
        self.switchPageLineEdit.setFixedWidth(40)

        switchPage = QLabel("转到第")
        page = QLabel("页")
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        operatorLayout.addWidget(switchPage)
        operatorLayout.addWidget(self.switchPageLineEdit)
        operatorLayout.addWidget(page)
        operatorLayout.addWidget(self.switchPageButton)
        operatorLayout.addWidget(QSplitter())

        statusLayout = QHBoxLayout()
        self.totalPageLabel = QLabel()
        self.totalPageLabel.setFixedWidth(70)
        self.currentPagelabel = QLabel()
        self.currentPagelabel.setFixedWidth(70)

        self.totalRecordLabel = QLabel()
        self.totalRecordLabel.setFixedWidth(70)

        statusLayout.addWidget(self.totalPageLabel)
        statusLayout.addWidget(self.currentPagelabel)
        statusLayout.addWidget(QSplitter())
        statusLayout.addWidget(self.totalRecordLabel)

        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(operatorLayout)
        mainLayout.addWidget(self.tableView)
        mainLayout.addLayout(statusLayout)
        self.setLayout(mainLayout)

    def setTableView(self):
        self.queryModel = QSqlQueryModel(self)
        self.currentPage = 1
        self.totalRecordCount = self.getTotalRecordCount()
        self.totalPage = self.getPageCount()
        self.updateStatus()
        self.setTotalPageLabel()
        self.setTotalRecordLabel()

        self.recordQuery(0)

        self.tableView.setModel(self.queryModel)

        print('totalRecordCount=' + str(self.totalRecordCount))
        print('totalPage=' + str(self.totalPage))

        self.queryModel.setHeaderData(0, Qt.Horizontal, "编号")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "姓名")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "性别")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "年龄")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "院系")

    def getTotalRecordCount(self):
        self.queryModel.setQuery("select * from student")
        rowCount = self.queryModel.rowCount()
        print('rowCount=' + str(rowCount))
        return rowCount

    def getPageCount(self):
        if self.totalRecordCount % self.PageRecordCount == 0:
            return (self.totalRecordCount / self.PageRecordCount)
        else:
            return (self.totalRecordCount / self.PageRecordCount + 1)

    def recordQuery(self, limitIndex):
        szQuery = ("select * from student limit %d,%d " % (limitIndex, self.PageRecordCount))
        print('query sql=' + szQuery)
        self.queryModel.setQuery(szQuery)

    def updateStatus(self):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPagelabel.setText(szCurrentText)

        if self.currentPage == 1:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
        elif self.currentPage == int(self.totalPage):
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    def setTotalPageLabel(self):
        szPageCountText = ("总共%d页" % self.totalPage)
        self.totalRecordLabel.setText(szPageCountText)

    def setTotalRecordLabel(self):
        szTotalRecordText = ("共%d条" % self.totalRecordCount)
        print('***setTotalRecordLabel szTotalRecordText=' + szTotalRecordText)
        self.totalRecordLabel.setText(szTotalRecordText)

    def onPrevButtonClick(self):
        print('***onPrevButtonClick')
        limitIndex = (self.currentPage - 2) * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage -= 1
        self.updateStatus()

    def onNextButtonClick(self):
        print('***onNextButtonClick')
        limitIndex = self.currentPage * self.PageRecordCount
        self.recordQuery(limitIndex)
        self.currentPage += 1
        self.updateStatus()

    def onSwitchPageButtonClick(self):
        szText = self.switchPageLineEdit.text()

        pageIndex = int(szText)

        if pageIndex > self.totalPage or pageIndex < 1:
            QMessageBox(self, "提示", "没有指定的页面，请重新输入")
            return

        limitIndex = (pageIndex - 1) * self.PageRecordCount

        self.recordQuery(limitIndex)

        self.currentPage = pageIndex

        self.updateStatus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = DateGrid()
    example.show()
    sys.exit(app.exec_())
