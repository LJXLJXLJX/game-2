from src.gameGuiTemplate import Ui_MainWindow
from src.Game import Game
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

import numpy as np
from time import sleep
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initBoard = np.random.randint(2, size=(50, 50))
        self.pause = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setSignals()


    def initGame(self):
        self.game = Game()
        m = self.ui.heightSpinBox.value()
        n = self.ui.widthSpinBox.value()

        text = self.ui.textEdit.toPlainText()
        if text != '':
            self.ReadText(text)

        elif m > 0 and n > 0:
            self.initBoard = np.random.randint(2, size=(m, n))


        self.game.board = self.initBoard

        live = self.ui.liveLineEdit.text()+' '
        dead = self.ui.deadLineEdit.text()+' '
        self.liveList=self.splitInt(live)
        self.deadList=self.splitInt(dead)


    def splitInt(self, L):
        res = []
        isNum = False
        for i in range(len(L)):
            if L[i] >= '0' and L[i] <= '9' and isNum == False:
                head = i
                isNum = True
            if (L[i] < '0' or L[i] > '9') and isNum == True:
                tail = i
                isNum = False
                res.append(int(L[head:tail]))
        return res

    def setSignals(self):
        self.ui.commitPushButton.clicked.connect(self.Start)
        self.ui.pausePushButton.clicked.connect(self.Pause)
        self.ui.stopPushButton.clicked.connect(self.Stop)

    def Start(self):


        self.initGame()
        self.pause = False
        self.Run()

    def Pause(self):
        if self.pause==False:
            self.pause = True
            self.ui.pausePushButton.setText("继续")


        elif self.pause==True:
            self.pause=False
            self.ui.pausePushButton.setText("暂停")
            self.Run()


    def Stop(self):
        self.pause = True
        cv2.destroyAllWindows()

    def Run(self):
        while not self.pause:
            self.game.update(live=self.liveList, dead=self.deadList)
            cv2.namedWindow('img', 0)
            cv2.imshow('img', self.game.board)
            cv2.waitKey(1)
            sleep(self.ui.speedSpinBox.value() / 100)
    def ReadText(self,text):
        text=text.split('\n')
        temp=[]
        for i in text:
            if i!='':
                temp.append(i)
        m=len(temp)
        if(m>0):
            n=len(temp[0])
        else:
            raise Exception("输入数据不规范！")
        self.game.board=np.zeros((m,n))
        for i in range(m):
            for j in range(n):
                self.game.board[i][j]=int(temp[i][i]>0)



    def test(self):
        self.ui.widthLabel.setText('999999')


if __name__ == '__main__':
    App = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(App.exec_())
