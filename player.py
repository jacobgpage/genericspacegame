'''
    this is the file for all things related to the player object
'''
from PyQt6.QtWidgets import QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

class player(QGraphicsPixmapItem):
    def __init__(self, image_name):
        super().__init__()

        # this is used to limit the player's ammo
        self.ammo = 25
        self.reload = 25
        self.image_name = image_name
        
        self.health = 100
        self.setPixmap(QPixmap(image_name))