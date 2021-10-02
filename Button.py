import pygame
import os
from Font import *
from defs import *
mainPath = os.path.dirname(__file__)
resourcesPath = os.path.join(mainPath, "resources")
imagesPath = os.path.join(resourcesPath, "images")
buttonImg = pygame.image.load(os.path.join(imagesPath, 'button.png'))
mainButton = pygame.transform.scale(buttonImg, (buttonImg.get_width()*8, buttonImg.get_height()*8))
gameFont = Font(os.path.join(imagesPath, 'font.png'))
class Button(object):
	def __init__(self, buttonX, buttonY, buttonText):
		self.buttonText = buttonText
		self.buttonX = buttonX
		self.buttonY = buttonY
		self._rect = pygame.Rect(buttonX, buttonY, mainButton.get_width(), mainButton.get_height())
	def draw(self, screen):
		screen.blit(mainButton, self._rect)
		gameFont.render(screen, self.buttonText, (self.buttonX*1.25, self.buttonY+18))