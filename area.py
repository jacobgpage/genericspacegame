'''
    area.py
    teamlit
    Creates a play window with two buttons (Pause and Exit), a player object, enemy bullets, and player bullets.
    The pause menu for the pause button is also implemented and includes four buttons (Resume, Main Menu, Restart, and Exit).
'''

from math import isqrt
import sys, random
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QPalette, QFont, QBrush, QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsScene, QMessageBox, QApplication
import player, bullet, windowmanager, main
import pygame

class Window(QGraphicsScene):
    def __init__(self):
        super().__init__(-50, -50, 600, 600)

        self.imageOneStartX = -250
        self.imageOneStartY = -1000
        self.imageTwoStartX = -250
        self.imageTwoStartY = -2919

        self.imageMove = 0

        # Controls whether the game is paused
        self.isPaused = True

        # The time elapsed since the start of the game, in seconds
        self.time = 0

        # The player's score, which is increased when the player kills an enemy ship.
        self.score = 0

        # Controls the number of enemy ships on screen at once and goes up over time
        self.intensity = 3

        # Used to measure when to increase intensity
        self.elapsed = 0

        # Used to measure how long between appearances bosses should spawn
        self.boss = 400

        # True if the player picked tutorial and false otherwise
        self.tutorial = bool

        # True if the player picked PvP mode and false otherwise
        self.pvp = bool


        # Create a widget with a button layout at the top right of the window
        topWidget = QWidget()

        self.topLayout = QVBoxLayout()
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.buttonLayout = QHBoxLayout()

        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Create the label that the time will be printed on
        self.displayTime = QLabel('Time: 0')
        self.displayTime.setFont(QFont("Times", 10, QFont.Weight.Medium))
        self.displayTime.setStyleSheet("background-color: white;"
                                        "color: black;"
                                        "min-width: 70 px;"
                                        "max-width: 70 px;"
                                        "min-height: 15 px;"
                                        "max-height: 15 px;"
                                        "padding: 3 px;")
        self.displayTime.setTextFormat(Qt.TextFormat.PlainText)
        self.buttonLayout.addWidget(self.displayTime)

        # Create the label that the score will be printed on
        self.displayScore = QLabel('Score: 0')
        self.displayScore.setFont(QFont("Times", 10, QFont.Weight.Medium))
        self.displayScore.setStyleSheet("background-color: white;"
                                        "color: black;"
                                        "min-width: 100 px;"
                                        "max-width: 100 px;"
                                        "min-height: 15 px;"
                                        "max-height: 15 px;"
                                        "padding: 3 px;")
        self.displayScore.setTextFormat(Qt.TextFormat.PlainText)
        self.buttonLayout.addWidget(self.displayScore)

        # Add a pause button to the button layout
        self.pauseButton = QPushButton()
        self.pauseButton.setText("Pause")
        self.pauseButton.setFont(QFont("Times", 10, QFont.Weight.Medium))
        self.pauseButton.setStyleSheet("background-color: lightGray;"
                                        "color: black;"
                                        "border-style: outset;"
                                        "border-width: 1px;"
                                        "border-color: black;"
                                        "min-width: 40 em;"
                                        "min-height: 15 em;"
                                        "max-height: 15 em;"
                                        "max-width: 40 em;"
                                        "padding: 6 px;")
        self.displayTime.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.pauseButton.clicked.connect(self.pauseClicked)                                
        self.buttonLayout.addWidget(self.pauseButton)
        
        # Add an exit button to the button layout
        self.exitButton = QPushButton()
        self.exitButton.setText("Exit")
        self.exitButton.setFont(QFont("Times", 10, QFont.Weight.Medium))
        self.exitButton.setStyleSheet("background-color: lightGray;"
                                        "color: black;"
                                        "border-style: outset;"
                                        "border-width: 1px;"
                                        "border-color: black;"
                                        "min-width: 40 em;"
                                        "max-width: 40 em;"
                                        "min-height: 15 em;"
                                        "max-height: 15 em;"
                                        "padding: 6 px;")
        self.exitButton.clicked.connect(self.exitClicked)
        self.buttonLayout.addWidget(self.exitButton)

        # Add a resume button to the button layout
        self.resumeButton = QPushButton()
        self.resumeButton.setText("Resume")
        self.resumeButton.setFont(QFont("Times", 10, QFont.Weight.Medium))
        self.resumeButton.setStyleSheet("background-color: lightGray;"
                                        "color: black;"
                                        "border-style: outset;"
                                        "border-width: 1px;"
                                        "border-color: black;"
                                        "min-width: 55 em;"
                                        "max-width: 55 em;"
                                        "min-height: 15 em;"
                                        "max-height: 15 em;"
                                        "padding: 6 px;")


        # Add the button layout to the widget and set the widget as the top widget
        self.topLayout.addLayout(self.buttonLayout)
        topWidget.setLayout(self.topLayout)

        # Set the size, location, and color of a widget which we call the top widget
        topWidget.setFixedSize(600, 50)
        topWidget.move(-50, -110)
        topWidgetPalette = topWidget.palette()
        topWidgetPalette.setColor(QPalette.ColorRole.Window, QColor(194, 197, 204))
        topWidget.setPalette(topWidgetPalette)

        #Creates widget at the bottom for the health bar
        self.healthBar = QWidget()
        self.healthBar.setGeometry(0, 570, 500, 30)
        healthBarPalette = self.healthBar.palette()
        healthBarPalette.setColor(QPalette.ColorRole.Window, QColor(0, 150, 0))
        self.healthBar.setPalette(healthBarPalette)

        self.displayHP = QLabel('HP') #Creates the label that "HP" is printed on
        self.displayHP.setFont(QFont("Times", 16, QFont.Weight.Medium))
        self.displayHP.setStyleSheet("background-color: rgba(0,0,0,0);"
                                        "color: white;"
                                        "min-width: 40 px;"
                                        "max-width: 40 px;"
                                        "min-height: 35 px;"
                                        "max-height: 35 px;"
                                        "padding: 3 px;")
        self.displayHP.setTextFormat(Qt.TextFormat.PlainText)
        self.displayHP.move(-40, 562)

        self.displayHealth = QLabel('100') #Creates the label that the health will be printed on
        self.displayHealth.setFont(QFont("Times", 16, QFont.Weight.Medium))
        self.displayHealth.setStyleSheet("background-color: rgba(0,0,0,0);"
                                        "color: white;"
                                        "min-width: 40 px;"
                                        "max-width: 40 px;"
                                        "min-height: 35 px;"
                                        "max-height: 35 px;"
                                        "padding: 3 px;")
        self.displayHealth.setTextFormat(Qt.TextFormat.PlainText)
        self.displayHealth.move(505, 562)

        self.image = QGraphicsPixmapItem()
        self.image.setPixmap(QPixmap("Images/milkyway.png"))
        self.addItem(self.image)

        self.imageTwo = QGraphicsPixmapItem()
        self.imageTwo.setPixmap(QPixmap("Images/milkyway.png"))
        self.addItem(self.imageTwo)

        self.addWidget(topWidget)
        self.addWidget(self.healthBar)
        self.addWidget(self.displayHP)
        self.addWidget(self.displayHealth)


        # Add player to the screen
        self.player = player.player(main.currentShip)
        self.player.setPos(self.width()/2-68, self.height()-100)
        self.addItem(self.player)
        
        # List of keys being pressed
        self.key_list = set()

        # List of bullets that the player shoots, it is added to on 'fireBullets'
        self.shotList = []

        # List of enemy ships that will be along the top of the screen
        self.enemyList = []

        # List of bullets that the enemies shoot at the player
        self.projectileList = []
        
    def pauseClicked(self):
        if not self.isPaused:
            # Create a message box to hold buttons to click when the game is paused
            self.pauseMenu = QMessageBox()
            self.pauseMenu.setText("{:^29}".format("Paused"))
            self.pauseMenu.setFont(QFont("Times", 14, QFont.Weight.Medium))
            self.pauseMenu.setStyleSheet("background-color: white;"
                                         "color: black;"
                                         "padding: 6px;")
            
            # Add the resume button to the pause menu
            self.pauseMenu.addButton(self.resumeButton, QMessageBox.ButtonRole.DestructiveRole)
            self.resumeButton.clicked.connect(self.resumeClicked)
            self.pauseMenu.setEscapeButton(self.resumeButton)

            # Add a main menu button to the pause menu
            self.menuButton = QPushButton()
            self.menuButton.setText("Main Menu")
            self.menuButton.setFont(QFont("Times", 10, QFont.Weight.Medium))
            self.menuButton.setStyleSheet("background-color: lightGray;"
                                          "color: black;"
                                          "border-style: outset;"
                                          "border-width: 1px;"
                                          "border-color: black;"
                                          "min-width: 70 em;"
                                          "max-width: 70 em;"
                                          "min-height: 15 em;"
                                          "max-height: 15 em;"
                                          "padding: 6 px;")
            self.menuButton.clicked.connect(self.menuClicked)
            self.pauseMenu.addButton(self.menuButton, QMessageBox.ButtonRole.DestructiveRole)

            # Add a restart button to the pause menu
            self.restartButton = QPushButton()
            self.restartButton.setText("Restart")
            self.restartButton.setFont(QFont("Times", 10, QFont.Weight.Medium))
            self.restartButton.setStyleSheet("background-color: lightGray;"
                                             "color: black;"
                                             "border-style: outset;"
                                             "border-width: 1px;"
                                             "border-color: black;"
                                             "min-width: 50 em;"
                                             "max-width: 50 em;"
                                             "min-height: 15 em;"
                                             "max-height: 15 em;"
                                             "padding: 6 px;")
            self.restartButton.clicked.connect(self.restartClicked)
            self.pauseMenu.addButton(self.restartButton, QMessageBox.ButtonRole.DestructiveRole)

            # Add an exit button to pauseMenu
            self.pauseExitButton = QPushButton()
            self.pauseExitButton.setText("Exit")
            self.pauseExitButton.setFont(QFont("Times", 10, QFont.Weight.Medium))
            self.pauseExitButton.setStyleSheet("background-color: lightGray;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 1px;"
                                            "border-color: black;"
                                            "min-width: 45 em;"
                                            "max-width: 45 em;"
                                            "min-height: 15 em;"
                                            "max-height: 15 em;"
                                            "padding: 6 px;")
            self.pauseExitButton.clicked.connect(self.exitClicked)
            self.pauseMenu.addButton(self.pauseExitButton, QMessageBox.ButtonRole.DestructiveRole)


            self.addWidget(self.pauseMenu)

            self.isPaused = True
                
            self.pauseMenu.open()

            # Move pauseMenu to the center of the scene
            centerX = int(self.sceneRect().center().x())
            centerY = int(self.sceneRect().center().y())
            self.pauseMenu.move(centerX - self.pauseMenu.width()/2, centerY - self.pauseMenu.width()/2)
    
    def resumeClicked(self):
        self.isPaused = False

    def restartClicked(self):
        self.deleteSelf()
        self.newWindow = windowmanager.MainMenuWindow()
        if self.tutorial == True:
            self.newWindow.tutorialClicked()
        elif self.pvp == True:
            self.newWindow.pvpClicked()
        else:
            self.newWindow.startGame()

    def menuClicked(self):
        self.deleteSelf()
        QApplication.closeAllWindows()

        self.newWindow = windowmanager.MainMenuWindow()
        self.newWindow.show()

    def exitClicked(self):
        sys.exit()

    def spawnEnemy(self, thing = "e"):
        # Updates the time, because spawnEnemy is called on a 1 second interval
        if self.tutorial == False and self.pvp == False:
            self.time += 1

        self.displayTime.setText("Time: " + str(self.time))
        if thing == "e":
            if (len(self.enemyList) < self.intensity):
                self.enemy, self.boss = bullet.getEnemy(self.enemyList, self.boss)
                self.addItem(self.enemy)
                self.enemyList.append(self.enemy)
        elif len(self.enemyList) < 3:
            self.enemy = bullet.getTutorialEnemy(len(self.enemyList), thing)
            if self.enemy is not None:
                self.addItem(self.enemy)
                self.enemyList.append(self.enemy)
            

    # Here, use x and y to determine the position the bullet will start at
    def firePressed(self, x, y, dir, player):
        if player.reload >= player.ammo:
            if dir == "up":
                self.fireBullets(x, y, "Images/beam2.png", self.shotList, -30)
            elif dir == "down":
                self.fireBullets(x, y, "Images/beam3.png", self.shotList2, 30)

            if main.globalIsMuted == False:
                    soundObject = pygame.mixer.Sound('Sounds/shoot.wav')
                    soundObject.set_volume(main.soundVolume)
                    soundObject.play()

    def fireBullets(self, x, y, image, shotList, speed):
        shot = bullet.bullet(x + 3, y, image, 0, speed)
        self.addItem(shot)
        shotList.append(shot)
        shot = bullet.bullet(x + 39, y, image, 0, speed)
        self.addItem(shot)
        shotList.append(shot)

    def keyPressEvent(self, event):
        if not self.isPaused:
            self.key_list.add(event.key())

    def keyReleaseEvent(self, event):
        if not self.isPaused:
            self.key_list.remove(event.key())

    def pvpInit(self):
        self.tutorial = False
        self.pvp = True

        self.removeItem(self.player)
        self.healthBar.deleteLater()
        self.displayHP.deleteLater()
        self.displayHealth.deleteLater()

        # player 1 is one more pixel to the right so they line up better at the start
        self.player1 = player.player("Images/fighter-red.png")
        self.player1.setPos(self.width()/2-69, self.height()-100)
        self.addItem(self.player1)
        self.player1.ammo = 8
        
        self.player2 = player.player("Images/fighter-blue-down.png")
        self.player2.setPos(self.width()/2-68, self.height()-650)
        self.addItem(self.player2)
        self.player2.ammo = 8
        self.shotList2 = []

        self.isPaused = False

    def tutorialInit(self):
        self.pvp = False
        self.tutorial = True

        self.removeItem(self.image)
        self.removeItem(self.imageTwo)
        self.removeItem(self.player)

        self.image3 = QGraphicsPixmapItem()
        self.image3.setPixmap(QPixmap("Images/Tutorial-Background.png"))
        self.addItem(self.image3)
        self.addItem(self.player)
        self.image3.setPos(-50, -60)

        self.isPaused = False

    def updateMovement(self):
        if not self.isPaused:
            # This is used for limiting the player's ammo
            # reload is incremented by 2 because otherwise the reload time is too slow
            self.player.reload += 2
            if len(self.shotList) >= self.player.ammo:
                self.player.reload = 0
            
            # This is used to stop bosses from appearing constantly
            self.boss += 1

            if self.displayScore is not None:
                self.displayScore.setText("Score: " + str(self.score))

            xVel = 0
            yVel = 0
            if Qt.Key.Key_P in self.key_list:
                self.pauseClicked()
                self.key_list.remove(Qt.Key.Key_P)
            if Qt.Key.Key_Left in self.key_list or Qt.Key.Key_A in self.key_list:
                # Change velocity
                xVel = -40
                
            if Qt.Key.Key_Right in self.key_list or Qt.Key.Key_D in self.key_list:
                # Change velocity
                xVel = 40

            if Qt.Key.Key_Up in self.key_list or Qt.Key.Key_W in self.key_list:
                # Change velocity
                yVel = -40

            if Qt.Key.Key_Down in self.key_list or Qt.Key.Key_S in self.key_list:
                # Change velocity
                yVel = 40

            if Qt.Key.Key_Space in self.key_list:
                # Fire bullet
                self.firePressed(self.player.x(), self.player.y(), "up", self.player)

            if self.tutorial == True:
                if Qt.Key.Key_1 in self.key_list:
                    self.spawnEnemy("1")
                if Qt.Key.Key_2 in self.key_list:
                    self.spawnEnemy("2")
                if Qt.Key.Key_3 in self.key_list:
                    self.spawnEnemy("3")
                if Qt.Key.Key_4 in self.key_list:
                    self.spawnEnemy("4")
                
            self.player.setPos(self.player.x()+xVel, self.player.y()+yVel)

            if self.player.x() > self.width()-118:
                self.player.setPos(self.width()-118, self.player.y())

            if self.player.x() < -50:
                self.player.setPos(-50, self.player.y())

            if self.player.y() > self.height()-100:
                self.player.setPos(self.player.x(), self.height()-100)

            if self.player.y() < 0:
                self.player.setPos(self.player.x(), 0)
            
            if self.tutorial == False:
                self.moveBackground()

            self.elapsed += 1
            if self.elapsed == 200:
                self.elapsed = 0
                self.intensity += 1
            
            if self.tutorial == False:
                self.score += 1 
            
            for item in self.enemyList:
                if item.shipType == 'b':
                    if item.y() >= 0:
                        item.yVel = 0
                        if item.once == 1:
                            item.xVel = random.randrange(-10, 10)
                            item.once = 0
                if item.shipType == 'c':
                    if item.y() <= -300:
                        item.yVel = self.intensity
                        if item.yVel > 4 or item.reload < 6:
                            item.yVel = 4
                            item.reload -= 1
                if item.shipType == 'd':
                    if item.y() >= -80:
                        item.yVel = 0
                        if item.once == 1:
                            item.xVel = 0
                            while (item.xVel == 0):
                                item.xVel = random.randrange(-4, 4)
                            item.once = 0
                item.shot += 1
                if item.shot > item.reload:
                        item.shot = 0

                item.setPos(item.x()+item.xVel, item.y()+item.yVel)
                collision = item.collidingItems()
                for bang in collision:

                    if isinstance(bang, type(self.player)):
                        self.soundObject = pygame.mixer.Sound('Sounds/hit.wav')
                        self.soundObject.set_volume(main.soundVolume)
                        self.soundObject.play()

                        self.player.health -= item.points
                        self.enemyList.remove(item)
                        self.removeItem(item)

                        if self.player.health <= 0:
                            if self.tutorial == True:
                                self.player.health = 100
                            else:
                                QApplication.closeAllWindows()

                                self.isPaused = True
                                self.deleteSelf()
                                self.windowmanager = windowmanager.EndWindow(self.score)
                                self.windowmanager.show()
                            

                if item.x() > self.width()-100:
                    item.xVel = -item.xVel
                    item.setPos(self.width()-100, item.y())

                if item.x() < -55:
                    item.xVel = -item.xVel
                    item.setPos(-55, item.y())
                
                if item.y() > self.height()+10:
                    self.enemyList.remove(item)
                    self.removeItem(item)

                if item.y() < -400:
                    item.yVel = -item.yVel
                    item.setPos(item.x(), -10)

                if item.shipType != 'd' and item.x() > self.width()-110:
                    item.xVel = -item.xVel
                    item.setPos(self.width()-110, item.y())

                elif item.shipType == 'd' and item.x() > self.width()-175:
                    item.xVel = -item.xVel
                    item.setPos(self.width()-175, item.y())


                if item.shot >= item.reload:
                    if item.shipType == 'b':
                        self.p = bullet.bullet(item.x() + 16, item.y(), "Images/beam3.png", 0, 30)
                        self.addItem(self.p)
                        self.projectileList.append(self.p)
                        if main.globalIsMuted == False:
                            soundObject = pygame.mixer.Sound('Sounds/laser.wav')
                            soundObject.set_volume(main.soundVolume)
                            soundObject.play()
                    elif item.shipType == 'c':
                        self.p = bullet.bullet(item.x() + 50, item.y() + 50, "Images/beam3.png", 0, 30)
                        if self.player.x() > item.x() + 80:
                            self.p.xVel += 5
                        elif self.player.x() < item.x() - 10:
                            self.p.xVel -= 5
                        item.reload = 10
                        self.addItem(self.p)
                        self.projectileList.append(self.p)
                        if main.globalIsMuted == False:
                            soundObject = pygame.mixer.Sound('Sounds/laser.wav')
                            soundObject.set_volume(main.soundVolume)
                            soundObject.play()
                    elif item.shipType == 'd':
                        item.reload = 18
                        self.p = bullet.bullet(item.x() + 28, item.y() + 69, "Images/beam4a.png", 0, 20)
                        self.addItem(self.p)
                        self.projectileList.append(self.p)
                        if main.globalIsMuted == False:
                            soundObject = pygame.mixer.Sound('Sounds/laser.wav')
                            soundObject.set_volume(main.soundVolume)
                            soundObject.play()

            for item in self.shotList:
                item.setPos(item.x()+item.xVel, item.y()+item.yVel)
                # -100 is the current limit, this could change
                if item.y() < -100:
                    self.shotList.remove(item)
                    self.removeItem(item)
                    continue
                collision = item.collidingItems()
                for bang in collision:
                    # This is easier than isinstance, and it works
                    if bang in self.enemyList:
                        bang.health -= 1
                        self.shotList.remove(item)
                        self.removeItem(item)
                        if bang.health == 0:
                            if self.tutorial == False:
                                self.score += bang.points
                            self.enemyList.remove(bang)
                            if bang.shipType == 'c' or bang.shipType == 'd':
                                # After the boss dies, we reset the timer so the player has about a minute without a boss on screen
                                self.boss = 0
                            self.removeItem(bang)
                            # Must break in case it collided with multiple enemies, since it will try to remove the bullet twice
                        break

            for item in self.projectileList:
                if item.image_name == "Images/beam4a.png":
                    if self.player.x() < item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4b.png", -5, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    elif self.player.x() > item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4e.png", 5, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    break
                elif item.image_name == "Images/beam4b.png":
                    if self.player.x() < item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4c.png", -10, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    elif self.player.x() > item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4a.png", 0, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    break
                elif item.image_name == "Images/beam4e.png":
                    if self.player.x() < item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4a.png", 0, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    elif self.player.x() > item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4f.png", 10, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    break
                elif item.image_name == "Images/beam4c.png":
                    if self.player.x() < item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4d.png", -15, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    elif self.player.x() > item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4b.png", -5, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    break
                elif item.image_name == "Images/beam4f.png":
                    if self.player.x() < item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4e.png", 5, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    elif self.player.x() > item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4g.png", 15, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                    break
                elif item.image_name == "Images/beam4d.png":
                    if self.player.x() > item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4c.png", -10, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                        break
                elif item.image_name == "Images/beam4g.png":
                    if self.player.x() < item.x():
                        self.j = bullet.bullet(item.x(), item.y(), "Images/beam4f.png", 10, 20)
                        self.projectileList.remove(item)
                        self.removeItem(item)
                        self.projectileList.append(self.j)
                        self.addItem(self.j)
                        break
                
            for item in self.projectileList:
                item.setPos(item.x() + item.xVel, item.y() + item.yVel)    
                if item.y() > self.height() + 10:
                    self.projectileList.remove(item)
                    self.removeItem(item)
                collision = item.collidingItems()
                for bang in collision:
                    if isinstance(bang, type(self.player)):
                        if self.tutorial == False:
                            self.player.health -= 15
                        self.projectileList.remove(item)
                        self.removeItem(item)

                        self.soundObject = pygame.mixer.Sound('Sounds/hit.wav')
                        self.soundObject.set_volume(main.soundVolume)
                        self.soundObject.play()

                        if self.player.health <= 0:
                            if self.tutorial == True:
                                self.player.health = 100
                            else:
                                QApplication.closeAllWindows()
                                
                                self.isPaused = True
                                self.deleteSelf()
                                self.windowmanager = windowmanager.EndWindow(self.score)
                                self.windowmanager.show()
            
            #Causes health bar widget to reflect health
            self.healthBar.setGeometry(0, 570, self.player.health*5, 30)
            self.displayHealth.setText(str(self.player.health))

    def updatePvPMovement(self):
        if not self.isPaused:
            self.player1.reload += 1
            self.player2.reload += 1
            if len(self.shotList) >= self.player1.ammo:
                self.player1.reload = 0
            if len(self.shotList2) >= self.player2.ammo:
                self.player2.reload = 0

            xVel1 = 0
            yVel1 = 0
            xVel2 = 0
            yVel2 = 0
            # player1 controls in pvp
            if Qt.Key.Key_W in self.key_list:
                yVel1 = -40
            if Qt.Key.Key_A in self.key_list:
                xVel1 = -40
            if Qt.Key.Key_S in self.key_list:
                yVel1 = 40
            if Qt.Key.Key_D in self.key_list:
                xVel1 = 40
            if Qt.Key.Key_Space in self.key_list:
                self.firePressed(self.player1.x(), self.player1.y(), "up", self.player1)
            
            # player2 controls in pvp
            if Qt.Key.Key_Up in self.key_list:
                yVel2 = -40
            if Qt.Key.Key_Left in self.key_list:
                xVel2 = -40
            if Qt.Key.Key_Down in self.key_list:
                yVel2 = 40
            if Qt.Key.Key_Right in self.key_list:
                xVel2 = 40
            if Qt.Key.Key_0 in self.key_list:
                # player 2's y here is increased so that it doesn't hit its own ship
                self.firePressed(self.player2.x(), self.player2.y() + 40, "down", self.player2)

            self.player1.setPos(self.player1.x()+xVel1, self.player1.y()+yVel1)
            self.player2.setPos(self.player2.x()+xVel2, self.player2.y()+yVel2)

            # player 1 boundaries
            if self.player1.x() > self.width()-119:
                self.player1.setPos(self.width()-119, self.player1.y())

            if self.player1.x() < -51:
                self.player1.setPos(-51, self.player1.y())

            if self.player1.y() > self.height()-50:
                self.player1.setPos(self.player1.x(), self.height()-50)

            if self.player1.y() < 300:
                self.player1.setPos(self.player1.x(), 300)
            
            # player 2 boundaries
            if self.player2.x() > self.width()-118:
                self.player2.setPos(self.width()-118, self.player2.y())

            if self.player2.x() < -50:
                self.player2.setPos(-50, self.player2.y())

            if self.player2.y() > 230:
                self.player2.setPos(self.player2.x(), 230)

            if self.player2.y() < 0:
                self.player2.setPos(self.player2.x(), 0)

            self.moveBackground()

            for item in self.shotList:
                item.setPos(item.x()+item.xVel, item.y()+item.yVel)
                if item.y() < -90:
                    self.shotList.remove(item)
                    self.removeItem(item)
                collision = item.collidingItems()
                for bang in collision:
                    if isinstance(bang, type(self.player)):
                        self.player2.health -= 10
                        self.shotList.remove(item)
                        self.removeItem(item)
                        if self.player2.health <= 0:
                            QApplication.closeAllWindows()

                            self.isPaused = True
                            self.deleteSelf()
                            self.windowmanager = windowmanager.pvpEndWindow("Player 1")
                            self.windowmanager.show()

            for item in self.shotList2:
                item.setPos(item.x()+item.xVel, item.y()+item.yVel)
                if item.y() > self.height() - 30:
                    self.shotList2.remove(item)
                    self.removeItem(item)
                collision = item.collidingItems()
                for bang in collision:
                    if isinstance(bang, type(self.player)):
                        self.player1.health -= 10
                        self.shotList2.remove(item)
                        self.removeItem(item)
                        if self.player1.health <= 0:
                            QApplication.closeAllWindows()

                            self.isPaused = True
                            self.deleteSelf()
                            self.windowmanager = windowmanager.pvpEndWindow("Player 2")
                            self.windowmanager.show()

    def moveBackground(self):
        self.imageMove += 2
        self.image.setPos(self.imageOneStartX, (self.imageOneStartY + self.imageMove))
        self.imageTwo.setPos(self.imageTwoStartX, (self.imageTwoStartY + self.imageMove))

        if (self.imageOneStartY + self.imageMove) >= 1080:
            self.imageOneStartY = -2749 - self.imageMove

        if (self.imageTwoStartY + self.imageMove) >= 1080:
            self.imageTwoStartY = -2749 - self.imageMove

    def updateTutorialBackground(self):
        self.setBackgroundBrush(QBrush(QColor(41, 61, 72)))

    def deleteSelf(self):
        if self.pvp == False:
            self.removeItem(self.player)
        else:
            self.removeItem(self.player1)
            self.removeItem(self.player2)
        self.enemyList.clear()
        self.shotList.clear()
        self.projectileList.clear()

        self.displayScore = None

        self.time = 0
        self.deleteLater()