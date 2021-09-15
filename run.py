#importing
import pygame
from pygame.locals import *
import info
from pymsgbox import *
import sys
import os

#window size confirm
sizeConfirm = confirm(text='Select window size:', title='Danger!', buttons=['640, 320', '1024, 768', '896, 640'])

#applying window size
if sizeConfirm == '640, 320':
	windowSize = (640, 320)
elif sizeConfirm == '1024, 768':
	windowSize = (1024, 768)
elif sizeConfirm == '896, 640':
	windowSize = (896, 640)
elif sizeConfirm == None:
	exit()

#variables
moveRight = False
musicState = "On"
moveLeft = False
jumpCount = 0
airTimer = 0
trueScroll = [0,0]
fails = 0
click = False
playerX = 100
playerY = 48
speed = 2
level = 1
music = True
showFPS = False
gameMenuActivated = False
pygame.init()

#window
pygame.display.set_caption('Danger!')
screen = pygame.display.set_mode(windowSize)
display = pygame.Surface((448, 320))

clock = pygame.time.Clock()

#setting resources folders
mainPath = os.path.dirname(__file__)
resourcesPath = os.path.join(mainPath, "resources")
imagesPath = os.path.join(resourcesPath, "images")
mapsPath = os.path.join(resourcesPath, "maps")
musicPath = os.path.join(resourcesPath, "music")
soundsPath = os.path.join(resourcesPath, "sounds")

#preloading sounds
beepSound = pygame.mixer.Sound(os.path.join(soundsPath, 'beep.wav'))

#loading images
grassImg = pygame.image.load(os.path.join(imagesPath, 'grass.png'))
dirtImg = pygame.image.load(os.path.join(imagesPath, 'dirt.png'))
playerImg = pygame.image.load(os.path.join(imagesPath, 'player.png'))
stoneImg = pygame.image.load(os.path.join(imagesPath, 'stone.png'))
checkbuttonEmpty = pygame.image.load(os.path.join(imagesPath, 'checkbutton_empty.png'))
checkbuttonChecked = pygame.image.load(os.path.join(imagesPath, 'checkbutton_checked.png'))
gameMenuImg = pygame.image.load(os.path.join(imagesPath, 'gameMenuUI.png'))

#player collision rect
playerRect = pygame.Rect(100,16,8,16)

#Functions/Classes

class Player(object):
	def __init__(self, playerX, playerY, playerMovement):
		self.playerX = playerX
		self.playerY = playerY
		self.speed = 2.4
		self.moveRight = False
		self.moveLeft = False
		self.jumpCount = 0
		self.airTimer = 0
		self.playerMovement = [0, 0]
	def draw(self, display):
		if self.moveRight == True:
			self.playerMovement[0] += self.speed
		if self.moveLeft == True:
			self.playerMovement[0] -= self.speed
		self.playerMovement[1] += self.jumpCount
		self.jumpCount += 0.1
		if self.jumpCount > 3:
			self.jumpCount = 3
		display.blit(playerImg, (self.playerX, self.playerY))

class Button(object):
	def __init__(self, buttonX, buttonY, buttonText):
		self.images = pygame.image.load(os.path.join(imagesPath, 'button.png'))
		self.buttonText = buttonText
		self.buttonX = buttonX
		self.buttonY = buttonY
		self.imagesScaled = pygame.transform.scale(self.images, (self.images.get_width()*8, self.images.get_height()*8))
		self._rect = pygame.Rect(buttonX, buttonY, self.imagesScaled.get_width(), self.imagesScaled.get_height())
	def draw(self, screen):
		screen.blit(self.imagesScaled, self._rect)
		gameFont.render(screen, self.buttonText, (self.buttonX*1.2, self.buttonY+17))

class CheckButton(object):
	def __init__(self, checkbuttonX, checkbuttonY, checkbuttonVariable):
		#importing checkbutton states
		self.checkbuttonVariable = checkbuttonVariable
		self.checkbuttonX = checkbuttonX
		self.checkbuttonY = checkbuttonY
		self.offStateImg = pygame.transform.scale(checkbuttonEmpty, (checkbuttonEmpty.get_width()*4, checkbuttonEmpty.get_height()*4))
		self.onStateImg = pygame.transform.scale(checkbuttonChecked, (checkbuttonChecked.get_width()*4, checkbuttonChecked.get_height()*4))
		if self.checkbuttonVariable == True:
			self._rect = pygame.Rect(checkbuttonX, checkbuttonY, self.onStateImg.get_width(), self.onStateImg.get_height())
		elif self.checkbuttonVariable == False:
			self._rect = pygame.Rect(checkbuttonX, checkbuttonY, self.offStateImg.get_width(), self.offStateImg.get_height())
	def draw(self, screen):
		if self.checkbuttonVariable == True:
			screen.blit(self.onStateImg, self._rect)
		elif self.checkbuttonVariable == False:
			screen.blit(self.offStateImg, self._rect)

def clip(surf,x,y,x_size,y_size):
	handle_surf = surf.copy()
	clipR = pygame.Rect(x,y,x_size,y_size)
	handle_surf.set_clip(clipR)
	image = surf.subsurface(handle_surf.get_clip())
	return image.copy()

class Font():
	def __init__(self, path):
		self.spacing = 1
		self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
		font_img = pygame.image.load(path)
		current_char_width = 0
		self.characters = {}
		character_count = 0
		in_gray = False
		for x in range(font_img.get_width()):
			c = font_img.get_at((x, 0))
			if c[0] == 127:
				if in_gray == False:
					char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
					self.characters[self.character_order[character_count]] = char_img.copy()
					character_count += 1
					current_char_width = 0
					in_gray = True
			else:
				current_char_width += 1
				in_gray = False
		self.space_width = self.characters['A'].get_width()

	def render(self, surf, text, loc):
		x_offset = 0
		for char in text:
			if char != ' ':
				surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
				x_offset += self.characters[char].get_width() + self.spacing
			else:
				x_offset += self.space_width + self.spacing

def loadMap(path):
	f = open((os.path.join(mapsPath, path)) + '.txt','r')
	data = f.read()
	f.close()
	data = data.split('\n')
	gameMap = []
	for row in data:
		gameMap.append(list(row))
	return gameMap

gameMap = loadMap('map' + str(level))

def collision_test(rect,tiles):
	hitList = []
	for tile in tiles:
		if rect.colliderect(tile):
			hitList.append(tile)
	return hitList

def move(rect,movement,tiles):
	collision_types = {'top':False,'bottom':False,'right':False,'left':False}
	rect.x += movement[0]
	hitList = collision_test(rect,tiles)
	for tile in hitList:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left'] = True
	rect.y += movement[1]
	hitList = collision_test(rect,tiles)
	for tile in hitList:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top'] = True
	return rect, collision_types

#fonts
bigFont = Font(os.path.join(imagesPath, 'Bigfont.png'))
gameFont = Font(os.path.join(imagesPath, 'font.png'))

player = Player(100, 48, speed)

#main menu buttons
buttonPlay = Button(340, 150, "Play")
buttonSettings = Button(340, 250, "Settings")

#settings buttons
musicChBt = CheckButton(470, 150, music)
showFPSChBt = CheckButton(510, 250, showFPS)
buttonBack = Button(330, 350, "Back")

#game menu buttons
resumeGame = Button(350, 100, "Resume")
saveGame = Button(350, 200, "Save")
settingsGameMenu = Button(350, 300, "Settings")
exitFromGame = Button(350, 400, "Exit")

def game(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerImg, gameMenuActivated):
	run = True
	while run:

		display.fill((146,244,255))

		trueScroll[0] += (playerRect.x-trueScroll[0]-152)/20
		trueScroll[1] += (playerRect.y-trueScroll[1]-106)/20
		scroll = trueScroll.copy()
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])


		tileRects = []
		y = 0
		for layer in gameMap:
			x = 0
			for tile in layer:
				if tile == "2":
					display.blit(dirtImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == "1":
					display.blit(grassImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == '3':
					display.blit(stoneImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile != "0":
					tileRects.append(pygame.Rect(x*16,y*16,16,16))
				x += 1
			y += 1

		playerMovement = [0, 0]
		if player.moveRight == True:
			playerMovement[0] += speed
			playerImg = pygame.image.load(os.path.join(imagesPath, 'player.png'))
		if player.moveLeft == True:
			playerMovement[0] -= speed
			playerImg = pygame.image.load(os.path.join(imagesPath, 'player2.png'))
		playerMovement[1] += player.jumpCount
		player.jumpCount += 0.2
		if jumpCount > 3:
			jumpCount = 3

		playerRect,collisions = move(playerRect,playerMovement,tileRects)

		if collisions['bottom'] == True:
			player.airTimer = 0
			player.jumpCount = 0
		else:
			player.airTimer += 1

		if collisions['top'] == True:
			player.airTimer = 0
			player.jumpCount = 0

		display.blit(playerImg,(playerRect.x-scroll[0],playerRect.y-scroll[1]))

		for event in pygame.event.get(): # event loop
			if event.type == QUIT:
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
					player.moveRight = True
				if event.key == K_LEFT:
					player.moveLeft = True
				if event.key == K_UP:
					if player.airTimer < 6:
						pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jump.wav')))
						pygame.mixer.Channel(0).set_volume(0.3)
						player.jumpCount = -5
				if event.key == K_ESCAPE:
					gameMenuActivated = True
			if event.type == KEYUP:
				if event.key == K_RIGHT:
					player.moveRight = False
				if event.key == K_LEFT:
					player.moveLeft = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if exitFromGame._rect.collidepoint(event.pos):
						pygame.mixer.music.stop()
						menu()
					elif resumeGame._rect.collidepoint(event.pos):
						gameMenuActivated = False
					elif settingsGameMenu._rect.collidepoint(event.pos):
						pygame.mixer.music.stop()
						settings(music, showFPS)
					elif saveGame._rect.collidepoint(event.pos):
						gameData = open(os.path.join(resourcesPath, "data"), "w")
						gameData.write(str(level))
						gameData.close()
						gameMenuActivated = False

		if playerRect.y > 800:
			pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
			fails += 1
			playerRect.x = 100
			playerRect.y = 16

		if level == 3:
			if playerRect.y == 144:
				pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
				fails += 1
				playerRect.x = 100
				playerRect.y = 16
			if playerRect.y == 352 and playerRect.x > 104:
				pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
				fails += 1
				playerRect.x = 100
				playerRect.y = 16

		if level == 4:
			if playerRect.y == 160:
				pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
				fails += 1
				playerRect.x = 100
				playerRect.y = 16

		if level != 4:
			if level != 5:
				if playerRect.x >= 1250:
					pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(soundsPath, 'complete.wav')))
					playerRect.x = 100
					playerRect.y = 16
					level += 1
					gameMap = loadMap('map' + str(level))

		if level == 5:
			if playerRect.y == 208:
				pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
				fails += 1
				playerRect.x = 100
				playerRect.y = 16

		screen.blit(pygame.transform.scale(display,windowSize),(0,0))
		player.draw(display)
		gameFont.render(screen, "Level "+str(level), (10, 10))
		gameFont.render(screen, "Fails: "+str(fails), (130, 10))
		if showFPSChBt.checkbuttonVariable == True:
			gameFont.render(screen, "FPS: "+str(int(clock.get_fps())), (10, 50))
		if gameMenuActivated == True:
			gameMenuUI = pygame.transform.scale(gameMenuImg, (gameMenuImg.get_width()*18, gameMenuImg.get_width()*18))
			screen.blit(gameMenuUI, (160, 35))
			exitFromGame.draw(screen)
			resumeGame.draw(screen)
			saveGame.draw(screen)
			settingsGameMenu.draw(screen)
		pygame.display.update()
		clock.tick(info.framerate)


#menu
def menu():
	run = True
	while run:
		screen.fill((146,244,255))
		bigFont.render(screen, "Danger!", (350, 50))

		buttonPlay.draw(screen)

		buttonSettings.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if buttonPlay._rect.collidepoint(event.pos):
						print(showFPS)
						if musicChBt.checkbuttonVariable == True:
							pygame.mixer.music.load(os.path.join(musicPath, 'soundtrack1.wav'))
							pygame.mixer.music.play(-1)
							pygame.mixer.music.set_volume(1)
						level = 1
						gameMap = loadMap('map' + str(level))
						playerRect.x, playerRect.y = (100, 16)
						game(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerImg, gameMenuActivated)
					elif buttonSettings._rect.collidepoint(event.pos):
						pygame.mixer.Channel(4).play(beepSound)
						settings(music, showFPS)

		pygame.display.update()
		clock.tick(60)

def settings(music, showFPS):
	run = True
	while run:
		screen.fill((146,244,255))

		bigFont.render(screen, "Settings", (335, 50))
		bigFont.render(screen, "Music ", (330, 150))
		bigFont.render(screen, "Show FPS", (280, 250))

		buttonBack.draw(screen)

		musicChBt.draw(screen)
		showFPSChBt.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					# musicChBt.stateChange()
					# showFPSChBt.stateChange()
					if musicChBt._rect.collidepoint(event.pos):
						if music == True:
							music = False
							musicChBt.checkbuttonVariable = music
							print("Music state is "+str(music))
						elif music == False:
							music = True
							musicChBt.checkbuttonVariable = music
							print("Music state is "+str(music))

					if showFPSChBt._rect.collidepoint(event.pos):
						if showFPS == True:
							showFPS = False
							showFPSChBt.checkbuttonVariable = showFPS
							print("ShowFPS state is "+str(showFPS))
						elif showFPS == False:
							showFPS = True
							showFPSChBt.checkbuttonVariable = showFPS
							print("ShowFPS state is "+str(showFPS))

					if buttonBack._rect.collidepoint(event.pos):
						print(showFPS)
						pygame.mixer.Channel(4).play(beepSound)
						menu()

		pygame.display.update()
		clock.tick(60)

menu()