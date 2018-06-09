import numpy as np
from time import sleep
import cv2


class Game:
    def __init__(self, *args,**kwargs):
        if len(args) == 0:
            self.board = np.zeros([50, 50], dtype=np.uint8)
        elif len(args) == 1:
            if type(args[0]) != np.ndarray:
                raise Exception("输入参数类型错误！单个参数时需要输入np.ndarray!")
            self.board = args[0]
        elif len(args) == 2:
            if type(args[0]) != int or type(args[1]) != int:
                raise Exception("输入参数类型错误！两个参数时需要输入两个int")
            self.board = np.zeros([args[0], args[1]], dtype=np.uint8)
        else:
            raise Exception("输入参数错误！")

    def update(self,**kwargs):
        temp = np.zeros(self.board.shape)
        for i in range(temp.shape[0]):
            for j in range(temp.shape[1]):
                neighbourNum = 0
                if i - 1 >= 0 and j - 1 >= 0 and self.board[i - 1][j - 1] == 1:
                    neighbourNum += 1
                if i - 1 >= 0 and self.board[i - 1][j] == 1:
                    neighbourNum += 1
                if i - 1 >= 0 and j + 1 <= temp.shape[1] - 1 and self.board[i - 1][j + 1] == 1:
                    neighbourNum += 1
                if j + 1 <= temp.shape[1] - 1 and self.board[i][j + 1] == 1:
                    neighbourNum += 1
                if i + 1 <= temp.shape[0] - 1 and j + 1 <= temp.shape[1] - 1 and self.board[i + 1][j + 1] == 1:
                    neighbourNum += 1
                if i + 1 <= temp.shape[0] - 1 and self.board[i + 1][j] == 1:
                    neighbourNum += 1
                if i + 1 <= temp.shape[0] - 1 and j - 1 >= 0 and self.board[i + 1][j - 1] == 1:
                    neighbourNum += 1

                liveList=[2,3]
                deadList=[3]
                if 'live' in kwargs.keys():
                    liveList=kwargs['live']
                if 'dead' in kwargs.keys():
                    deadList=kwargs['dead']

                if self.board[i][j] == 1 and neighbourNum in liveList:
                    temp[i][j] = 1
                elif self.board[i][j] == 0 and neighbourNum in deadList:
                    temp[i][j] = 1
        self.board = temp


    def run(self):
        while True:
            self.update(live=[3,4,5])
            cv2.namedWindow('img',0)
            cv2.imshow('img',self.board)
            # sleep(0.5)
            cv2.waitKey(2)


if __name__ == '__main__':
    board = np.random.randint(2,size=(50,50))
    game = Game(board)
    game.run()
    print(game.board)
