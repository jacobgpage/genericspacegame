'''
    this is the file for bullet objects
'''
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
import random

class bullet(QGraphicsPixmapItem):
    def __init__(self, x_pos, y_pos, image_name, x_vel, y_vel):
        super().__init__()
        self.image_name = image_name
        self.setPixmap(QPixmap(image_name))
        self.setX(x_pos)
        self.setY(y_pos)
        self.xVel = x_vel
        self.yVel = y_vel

class ship(QGraphicsPixmapItem):
    def __init__(self, x_pos, y_pos, shipType, x_vel, y_vel, health):
        super().__init__()

        self.shipType = shipType
        if self.shipType == 'a':
            image_name = "Images/enemy2.png"
        elif self.shipType == 'b':
            image_name = "Images/enemy.png"
        elif self.shipType == 'c':
            image_name = "Images/BatMk3.png"
        elif self.shipType == 'd':
            image_name = "Images/Omega.png"

        self.setPixmap(QPixmap(image_name))

        self.once = 1
        self.health = health
        self.points = health * 20
        self.setX(x_pos)
        self.setY(y_pos)
        self.xVel = x_vel
        self.yVel = y_vel

        #this counts to a random number before shooting a bullet at the player
        self.shot = 0
        self.reload = random.randrange(4,20)

def getEnemy(enemyList, boss):
    enemyType = random.randrange(0,11)
    check = True
    for i in enemyList:
        if i.shipType == 'c' or i.shipType == 'd':
            check = False
    if enemyType <= 4:
        enemy = ship(random.randrange(0, 480), -300, 'b', 0, 20, 1)
    elif enemyType <= 9:
        enemy = ship(random.randrange(0, 480), -300, 'a', 0, 10, 3)
    elif enemyType == 10 and check == True and boss > 400:
        boss = 0
        enemyType = random.randrange(0,4)
        if enemyType <= 2:
            enemy = ship(180, -400, 'c', 0, 10, 50)
        if enemyType == 3:
            enemy = ship(180, -400, 'd', 0, 10, 80)
    else:
        enemy = ship(random.randrange(0, 480), -300, 'b', 0, 40, 1)
    return enemy, boss

def getTutorialEnemy(enemyListLength, thing):
    if thing == "1":
        enemy = ship(random.randrange(0,480), -300, 'b', 0, 20, 1)
        return enemy
    elif thing == "2":
        enemy = ship(random.randrange(0, 480), -300, 'a', 0, 10, 3)
        return enemy
    elif enemyListLength < 1:
        if thing == "3":
            enemy = ship(180, -400, 'c', 0, 10, 50)
            return enemy
        elif thing == "4":
            enemy = ship(180, -400, 'd', 0, 10, 80)
            return enemy