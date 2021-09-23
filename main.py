import pygame

while True:
	pygame.init()
	import os
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 30)
	import distutils
	from distutils import util
	mainPath = os.path.dirname(__file__)
	resourcesPath = os.path.join(mainPath, "resources")
	dataLoad = []
	with open(os.path.join(resourcesPath, 'data'), 'r') as filehandle:
		for line in filehandle:
			currentPlace = line[:-1]

			dataLoad.append(currentPlace)
	data = dataLoad
	print(data)
	fullscreen = bool(distutils.util.strtobool(data[4]))
	windowSize = (896, 640)
	pygame.display.set_caption('Danger!')
	if fullscreen == True:
		screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(windowSize)
	display = pygame.Surface((448, 320))
	imagesPath = os.path.join(resourcesPath, "images")
	musicPath = os.path.join(resourcesPath, "music")
	soundsPath = os.path.join(resourcesPath, "sounds")
	#loading images
	logoImg = pygame.image.load(os.path.join(imagesPath, 'logo.png'))
	backgroundImg = pygame.image.load(os.path.join(imagesPath, 'bg.png')).convert()
	background = pygame.transform.scale(backgroundImg, (backgroundImg.get_width()*8, backgroundImg.get_height()*8))
	grassImg = pygame.image.load(os.path.join(imagesPath, 'grass.png')).convert()
	dirtImg = pygame.image.load(os.path.join(imagesPath, 'dirt.png')).convert()
	playerImg = pygame.image.load(os.path.join(imagesPath, 'player.png'))
	stoneImg = pygame.image.load(os.path.join(imagesPath, 'stone.png')).convert()
	spikeImg = pygame.image.load(os.path.join(imagesPath, 'spikes.png'))
	finishFlagImg = pygame.image.load(os.path.join(imagesPath, 'finish-flag.png'))
	checkpointFlagImg = pygame.image.load(os.path.join(imagesPath, 'checkpoint-flag.png'))
	bridgeLeftImg = pygame.image.load(os.path.join(imagesPath, 'bridge-left.png'))
	bridgeRightImg = pygame.image.load(os.path.join(imagesPath, 'bridge-right.png'))
	bridgeCenterImg = pygame.image.load(os.path.join(imagesPath, 'bridge-center.png'))
	checkbuttonEmpty = pygame.image.load(os.path.join(imagesPath, 'checkbutton_empty.png'))
	checkbuttonChecked = pygame.image.load(os.path.join(imagesPath, 'checkbutton_checked.png'))
	gameMenuImg = pygame.image.load(os.path.join(imagesPath, 'gameMenuUI.png'))
	cursorImg = pygame.image.load(os.path.join(imagesPath, 'cursor.png'))
	buttonImg = pygame.image.load(os.path.join(imagesPath, 'button.png'))
	mainButton = pygame.transform.scale(buttonImg, (buttonImg.get_width()*8, buttonImg.get_height()*8))
	screen.blit(logoImg, (448-logoImg.get_width()/2, 320-logoImg.get_height()/2))
	pygame.display.update()
	from pygame.locals import *
	import sys
	import time
	import random
	from defs import *
	break

# variables
moveRight = False
musicState = "On"
moveLeft = False
jumpCount = 0
airTimer = 0
trueScroll = [0,0]
fails = 0
playerX = 100
playerY = 48
speed = 2
level = 1
checkpointPosition = [0, 0]
checkpointed = False
spikesObjectCount = 0
music = bool(distutils.util.strtobool(data[1]))
showFPS = bool(distutils.util.strtobool(data[3]))
sfx = bool(distutils.util.strtobool(data[2]))
gameMenuActivated = False
f3Menu = False

backgroundData = [(146,244,255),(48, 53, 66)] 
if data[5] == "ru":
	lang = ["Играть",
			"Настройки",
			"О игре",
			"Выйти",
			"Назад",
			"Продолжить",
			"Сохранить",
			"Новая игра",
			"Загрузить",
			"Уровни",
			"Выживание",
			"Уровень ",
			"Неудач: ",
			"Музыка",
			"SFX",
			"Вид",
			"Язык",
			"Звук",
			"Показывать FPS",
			"Полный экран",
			"Создатель: FireFall",
			"Используемые программы:",
			"FL Studio",
			"Sublime Text 3",
			"Python 3.7.3",
			"Aseprite",
			"Tiled",
			"Репорт"]
else:
	lang = ["Play",
			"Settings",
			"About",
			"Exit",
			"Back",
			"Resume",
			"Save",
			"New Game",
			"Load Game",
			"Levels",
			"Survival",
			"Level ",
			"Fails: ",
			"Music",
			"SFX",
			"View",
			"Language",
			"Sound",
			"Show FPS",
			"Fullscreen",
			"Main Creator: FireFall",
			"Used Programs:",
			"FL Studio",
			"Sublime Text 3",
			"Python 3.7.3",
			"Aseprite",
			"Tiled",
			"Report"]

gameMap = {}

clock = pygame.time.Clock()

#preloading sounds
beepSound = pygame.mixer.Sound(os.path.join(soundsPath, 'beep.wav'))

tileIndex = {1:grassImg, 2:dirtImg}

#resizing loaded images
cursor = pygame.transform.scale(cursorImg, (cursorImg.get_width()*2, cursorImg.get_height()*2))

pygame.display.set_icon(playerImg)

#player collision rect
playerRect = pygame.Rect(56,16,8,16)

#Functions/Classes
class Player(object):
	def __init__(self, playerX, playerY, playerMovement):
		self.playerX = playerX
		self.playerY = playerY
		self.speed = 3
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
		self.buttonText = buttonText
		self.buttonX = buttonX
		self.buttonY = buttonY
		self._rect = pygame.Rect(buttonX, buttonY, mainButton.get_width(), mainButton.get_height())
	def draw(self, screen):
		screen.blit(mainButton, self._rect)
		gameFont.render(screen, self.buttonText, (self.buttonX*1.25, self.buttonY+18))

class CheckButton(object):
	def __init__(self, checkbuttonX, checkbuttonY, checkbuttonVariable):
		self.checkbuttonEmpty = pygame.image.load(os.path.join(imagesPath, 'checkbutton_empty.png'))
		self.checkbuttonChecked = pygame.image.load(os.path.join(imagesPath, 'checkbutton_checked.png'))
		self.checkbuttonVariable = checkbuttonVariable
		self.checkbuttonX = checkbuttonX
		self.checkbuttonY = checkbuttonY
		self.offStateImg = pygame.transform.scale(self.checkbuttonEmpty, (self.checkbuttonEmpty.get_width()*4, self.checkbuttonEmpty.get_height()*4))
		self.onStateImg = pygame.transform.scale(self.checkbuttonChecked, (self.checkbuttonChecked.get_width()*4, self.checkbuttonChecked.get_height()*4))
		if self.checkbuttonVariable == True:
			self._rect = pygame.Rect(checkbuttonX, checkbuttonY, self.onStateImg.get_width(), self.onStateImg.get_height())
		else:
			self._rect = pygame.Rect(checkbuttonX, checkbuttonY, self.offStateImg.get_width(), self.offStateImg.get_height())
	def draw(self, screen):
		if self.checkbuttonVariable == True:
			screen.blit(self.onStateImg, self._rect)
		else:
			screen.blit(self.offStateImg, self._rect)

class Font():
	def __init__(self, path):
		self.spacing = 1
		self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',"А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь","э", "ю", "я",'.','-',',',':','+',"'",'!','?','0','1','2','3','4','5','6','7','8','9']
		font_img_org = pygame.image.load(path)
		font_img = pygame.transform.scale(font_img_org, (font_img_org.get_width()*2, font_img_org.get_height()*2))
		current_char_width = 0
		self.characters = {}
		character_count = 0
		is_transparent = False
		in_gray = False
		font_width = font_img.get_width()
		for x in range(font_width):
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

#fonts
bigFont = Font(os.path.join(imagesPath, 'bigFont.png'))
gameFont = Font(os.path.join(imagesPath, 'font.png'))
grayFont = Font(os.path.join(imagesPath, 'grayFont.png'))

player = Player(100, 48, speed)

#menu buttons
buttonPlay = Button(448-mainButton.get_width()/2, 150, lang[0])
buttonSettings = Button(448-mainButton.get_width()/2, 250, lang[1])
buttonAbout = Button(448-mainButton.get_width()/2, 350, lang[2])
exitGame = Button(448-mainButton.get_width()/2, 450, lang[3])

#settings buttons
langSettingButton = Button(170, 150, lang[16])
viewSettingButton = Button(450, 150, lang[15])
soundSettingButton = Button(170, 250, lang[17])
musicChBt = CheckButton(550, 150, music)
sfxChBt = CheckButton(550, 250, sfx)
showFPSChBt = CheckButton(550, 150, showFPS)
fullscreeenChBt = CheckButton(550, 250, fullscreen)
buttonBack = Button(350, 550, lang[4])

#gameMenu buttons
resumeGame = Button(448-mainButton.get_width()/2, 100, lang[5])
saveGame = Button(448-mainButton.get_width()/2, 200, lang[6])
settingsGameMenu = Button(448-mainButton.get_width()/2, 300, lang[1])
exitFromGame = Button(448-mainButton.get_width()/2, 400, lang[3])

#selectMode buttons
newGame = Button(350, 100, lang[7])
loadGame = Button(350, 200, lang[8])

#createGame buttons
createLevelsMode = Button(448-mainButton.get_width()/2, 100, lang[9])

buttonBack2 = Button(350, 500, lang[4])

reportButton = Button(350, 400, lang[27])

def levelsMode(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerImg, gameMenuActivated, f3Menu, checkpointed):

	run = True
	finish = False
	while run:

		if level == 6:
			display.fill(backgroundData[1])
		elif level == 7:
			display.fill(backgroundData[1])
		else:
			display.fill(backgroundData[0])

		trueScroll[0] += (playerRect.x-trueScroll[0]-152)/20
		trueScroll[1] += (playerRect.y-trueScroll[1]-106)/20
		scroll = trueScroll.copy()
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])

		
		tileRects = []
		spike_rects = []
		finish_flag_rects = []
		checkpoint_flag_rects = []
		y = 0
		spikesObjectCount = 0
		for layer in gameMap:
			x = 0
			for tile in layer:
				if tile == "1":
					display.blit(grassImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == "2":
					display.blit(dirtImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == '3':
					display.blit(stoneImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == '4':
					display.blit(bridgeLeftImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == '5':
					display.blit(bridgeRightImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == '6':
					display.blit(bridgeCenterImg,(x*16-scroll[0],y*16-scroll[1]))
				if tile == '7':
					display.blit(spikeImg, (x*16-scroll[0],y*16-scroll[1]))
					spike_rects.append(pygame.Rect(x*16,y*16,16,16))
				if tile == "8":
					display.blit(finishFlagImg, (x*16-scroll[0],y*16-scroll[1]))
					finish_flag_rects.append(pygame.Rect(x*16,y*16,16,16))
				if tile == "9":
					display.blit(checkpointFlagImg, (x*16-scroll[0],y*16-scroll[1]))
					checkpoint_flag_rects.append(pygame.Rect(x*16,y*16,16,16))
				if tile != "0" and tile != '7' and tile != '8' and tile != '9':
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

		hitList = collision_test(playerRect,spike_rects)
		for tile in hitList:
			if sfxChBt.checkbuttonVariable == True:
				pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
				fails += 1
				if checkpointed == False:
					playerRect.x = 80
					playerRect.y = 32
				else:
					playerRect.x, playerRect.y = checkpointPosition
		hitList = collision_test(playerRect,finish_flag_rects)
		for tile in hitList:
			if sfxChBt.checkbuttonVariable == True:
				pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(soundsPath, 'complete.wav')))
				playerRect.x = 80
				playerRect.y = 32
				level += 1
				gameMap = loadMap('map' + str(level))
		hitList = collision_test(playerRect,checkpoint_flag_rects)
		for tile in hitList:
			checkpointPosition = playerRect.x, playerRect.y
			checkpointed = True

		for event in pygame.event.get(): # event loop
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
					player.moveRight = True
				if event.key == K_LEFT:
					player.moveLeft = True
				if event.key == K_UP:
					if player.airTimer < 6:
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jump.wav')))
							pygame.mixer.Channel(0).set_volume(0.3)
						player.jumpCount = -5
				if event.key == K_d:
					player.moveRight = True
				if event.key == K_a:
					player.moveLeft = True
				if event.key == K_r:
					if sfxChBt.checkbuttonVariable == True:
						pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
						fails += 1
						if checkpointed == False:
							playerRect.x = 80
							playerRect.y = 32
						else:
							playerRect.x, playerRect.y = checkpointPosition
				if event.key == K_SPACE:
					if player.airTimer < 6:
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jump.wav')))
							pygame.mixer.Channel(0).set_volume(0.3)
						player.jumpCount = -5
				if event.key == K_w:
					if player.airTimer < 6:
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jump.wav')))
							pygame.mixer.Channel(0).set_volume(0.3)
						player.jumpCount = -5
				if event.key == K_ESCAPE:
					gameMenuActivated = True
				if event.key == K_F3:
					if f3Menu == True:
						f3Menu = False
					elif f3Menu == False:
						f3Menu = True
			if event.type == KEYUP:
				if event.key == K_RIGHT:
					player.moveRight = False
				if event.key == K_LEFT:
					player.moveLeft = False
			if event.type == KEYUP:
				if event.key == K_d:
					player.moveRight = False
				if event.key == K_a:
					player.moveLeft = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if exitFromGame._rect.collidepoint(event.pos):
						pygame.mixer.music.stop()
						if musicChBt.checkbuttonVariable == True:
							pygame.mixer.music.load(os.path.join(musicPath, 'mainTheme.ogg'))
							pygame.mixer.music.play(-1)
							pygame.mixer.music.set_volume(0.3)
						menu()
					elif resumeGame._rect.collidepoint(event.pos):
						pygame.mixer.music.unpause()
						gameMenuActivated = False
					elif settingsGameMenu._rect.collidepoint(event.pos):
						pygame.mixer.music.stop()
						settings(music, sfx, showFPS, fullscreen, screen)
					elif saveGame._rect.collidepoint(event.pos):
						gameData = open(os.path.join(resourcesPath, "data"), "w")
						gameData.write(str(level+"\n"+playerRect.x, playerRect.y))
						gameData.close()
						gameMenuActivated = False

		if level != 7:
			if playerRect.y > 800:
				if sfxChBt.checkbuttonVariable == True:
					pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(soundsPath, 'fail.wav')))
				fails += 1
				if checkpointed == False:
					playerRect.x = 80
					playerRect.y = 32
				else:
					playerRect.x, playerRect.y = checkpointPosition

		if level == 5:
			if playerRect.x > 4786:
				if sfxChBt.checkbuttonVariable == True:
					if musicChBt.checkbuttonVariable == True:
							pygame.mixer.music.load(os.path.join(musicPath, 'soundtrack2.ogg'))
							pygame.mixer.music.play(-1)
							pygame.mixer.music.set_volume(1)
					pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(soundsPath, 'complete.wav')))
					playerRect.x = 40
					playerRect.y = 80
					level += 1
					gameMap = loadMap('map' + str(level))

		screen.blit(pygame.transform.scale(display,windowSize),(0,0))
		player.draw(display)
		gameFont.render(screen, lang[11]+str(level), (10, 10))
		gameFont.render(screen, lang[12]+str(fails), (150, 10))
		if showFPSChBt.checkbuttonVariable == True:
			gameFont.render(screen, "FPS: "+str(int(clock.get_fps())), (10, 50))
		if gameMenuActivated == True:
			pygame.mixer.pause()
			pygame.mixer.music.pause()
			gameMenuUI = pygame.transform.scale(gameMenuImg, (gameMenuImg.get_width()*18, gameMenuImg.get_width()*18))
			screen.blit(gameMenuUI, (160, 35))
			exitFromGame.draw(screen)
			resumeGame.draw(screen)
			saveGame.draw(screen)
			settingsGameMenu.draw(screen)
			screen.blit(cursor, pygame.mouse.get_pos())
		if f3Menu == True:
			gameFont.render(screen, "X: "+str(playerRect.x)+" "+"Y: "+str(playerRect.y), (10, 90))

		pygame.display.update()
		clock.tick(60)

#menu
def menu():
	run = True
	while run:
		screen.fill((146,244,255))

		pygame.mouse.set_visible(False)

		screen.blit(background, (0,0))
		buttonPlay.draw(screen)
		buttonSettings.draw(screen)
		buttonAbout.draw(screen)
		exitGame.draw(screen)

		gameFont.render(screen, "0.4", (0, 616))

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if buttonPlay._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						selectMode()
					elif buttonSettings._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						settings(music, sfx, showFPS, fullscreen, screen)
					elif buttonAbout._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						about()
					elif exitGame._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						sys.exit()

		screen.blit(logoImg, (315, 5))
		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def settings(music, sfx, showFPS, fullscreen, screen):
	run = True
	while run:
		screen.fill((146,244,255))

		bigFont.render(screen, lang[1], (330, 50))

		buttonBack.draw(screen)
		langSettingButton.draw(screen)
		soundSettingButton.draw(screen)
		viewSettingButton.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if langSettingButton._rect.collidepoint(event.pos):
						langSettings()
					elif soundSettingButton._rect.collidepoint(event.pos):
						soundSettings(music, sfx)
					elif viewSettingButton._rect.collidepoint(event.pos):
						viewSettings(showFPS, fullscreen, screen)
					if musicChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if music == True:
							music = False
							data[1] = False
							musicChBt.checkbuttonVariable = music
						else:
							music = True
							data[1] = True
							musicChBt.checkbuttonVariable = music

					elif showFPSChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if showFPS == True:
							showFPS = False
							data[3] = False
							showFPSChBt.checkbuttonVariable = showFPS
						else:
							showFPS = True
							data[3] = True
							showFPSChBt.checkbuttonVariable = showFPS

					elif sfxChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if sfx == True:
							sfx = False
							data[2] = False
							sfxChBt.checkbuttonVariable = sfx
						else:
							sfx = True
							data[2] = True
							sfxChBt.checkbuttonVariable = sfx

					elif fullscreeenChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if fullscreen == True:
							fullscreen = False
							data[4] = False
							fullscreeenChBt.checkbuttonVariable = fullscreen
							screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
						else:
							fullscreen = True
							data[4] = True
							fullscreeenChBt.checkbuttonVariable = fullscreen
							screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)

					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						menu()

				with open(os.path.join(resourcesPath, 'data'), 'w') as filehandle:  
					for listitem in data:
						filehandle.write('%s\n' % listitem)

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def viewSettings(showFPS, fullscreen, screen):
	run = True
	while run:
		screen.fill((146,244,255))

		bigFont.render(screen, lang[15], (330, 50))
		bigFont.render(screen, lang[18], (150, 150))
		bigFont.render(screen, lang[19], (150, 250))

		buttonBack.draw(screen)

		showFPSChBt.draw(screen)
		fullscreeenChBt.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if showFPSChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if showFPS == True:
							showFPS = False
							data[3] = False
							showFPSChBt.checkbuttonVariable = showFPS
						else:
							showFPS = True
							data[3] = True
							showFPSChBt.checkbuttonVariable = showFPS

					elif fullscreeenChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if fullscreen == True:
							fullscreen = False
							data[4] = False
							fullscreeenChBt.checkbuttonVariable = fullscreen
							screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
						else:
							fullscreen = True
							data[4] = True
							fullscreeenChBt.checkbuttonVariable = fullscreen
							screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)

					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						settings(music, sfx, showFPS, fullscreen, screen)

				with open(os.path.join(resourcesPath, 'data'), 'w') as filehandle:  
					for listitem in data:
						filehandle.write('%s\n' % listitem)

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def soundSettings(music, sfx):
	run = True
	while run:
		screen.fill((146,244,255))

		bigFont.render(screen, lang[17], (330, 50))
		bigFont.render(screen, lang[13], (280, 150))
		bigFont.render(screen, lang[14], (280, 250))

		buttonBack.draw(screen)

		musicChBt.draw(screen)
		sfxChBt.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if musicChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if music == True:
							music = False
							data[1] = False
							musicChBt.checkbuttonVariable = music
						else:
							music = True
							data[1] = True
							musicChBt.checkbuttonVariable = music

					elif sfxChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if sfx == True:
							sfx = False
							data[2] = False
							sfxChBt.checkbuttonVariable = sfx
						else:
							sfx = True
							data[2] = True
							sfxChBt.checkbuttonVariable = sfx

					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						settings(music, sfx, showFPS, fullscreen, screen)

				with open(os.path.join(resourcesPath, 'data'), 'w') as filehandle:  
					for listitem in data:
						filehandle.write('%s\n' % listitem)

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def langSettings():
	run = True
	while run:
		screen.fill((146,244,255))

		bigFont.render(screen, lang[16], (330, 50))
		engRect = pygame.Rect(330, 150, 162, 64)
		ruRect = pygame.Rect(330, 220, 162, 64)
		buttonBack.draw(screen)
		if data[5] == "en":
			bigFont.render(screen, "English", (330, 150))
		else:
			grayFont.render(screen, "English", (330, 150))
		if data[5] == "ru":
			bigFont.render(screen, "Russian", (330, 220))
		else:
			grayFont.render(screen, "Russian", (330, 220))

		gameFont.render(screen, "Language will change after restarting program!", (200, 320))

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if engRect.collidepoint(event.pos):
						data[5] = "en"
					elif ruRect.collidepoint(event.pos):
						data[5] = "ru"
					elif buttonBack._rect.collidepoint(event.pos):
						settings(music, sfx, showFPS, fullscreen, screen)

				with open(os.path.join(resourcesPath, 'data'), 'w') as filehandle:  
					for listitem in data:
						filehandle.write('%s\n' % listitem)

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def selectMode():
	run = True
	while run:
		screen.fill((146, 244, 255))

		newGame.draw(screen)
		loadGame.draw(screen)
		buttonBack.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if newGame._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						createGame()
					elif loadGame._rect.collidepoint(event.pos):
						level = int(data[0])
						print(level)
						gameMap = loadMap('map' + str(level))
						pygame.mixer.music.stop()
						if musicChBt.checkbuttonVariable == True:
							if level >= 6:
								pygame.mixer.music.load(os.path.join(musicPath, 'soundtrack2.ogg'))
							else:
								pygame.mixer.music.load(os.path.join(musicPath, 'soundtrack1.ogg'))
							pygame.mixer.music.play(-1)
							pygame.mixer.music.set_volume(1)
						levelsMode(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerImg, gameMenuActivated, f3Menu, checkpointed)
					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						menu()

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def createGame():
	run = True
	while run:
		screen.fill((146, 244, 255))

		createLevelsMode.draw(screen)
		buttonBack.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if createLevelsMode._rect.collidepoint(event.pos):
						pygame.mixer.music.stop()
						if musicChBt.checkbuttonVariable == True:
							pygame.mixer.music.load(os.path.join(musicPath, 'soundtrack1.ogg'))
							pygame.mixer.music.play(-1)
							pygame.mixer.music.set_volume(1)
						level = 1
						gameMap = loadMap('map' + str(level))
						levelsMode(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerImg, gameMenuActivated, f3Menu, checkpointed)
					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						selectMode()

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def about():
	run = True
	while run:
		screen.fill((146,244,255))

		bigFont.render(screen, lang[2], (370, 50))
		gameFont.render(screen, lang[20], (300, 120))
		gameFont.render(screen, lang[21], (300, 190))
		gameFont.render(screen, "FL Studio", (300, 230))
		gameFont.render(screen, "Sublime Text 3", (300, 260))
		gameFont.render(screen, "Python 3.7.3", (300, 290))
		gameFont.render(screen, "Aseprite", (300, 320))
		gameFont.render(screen, "Tiled", (300, 350))

		reportButton.draw(screen)
		buttonBack2.draw(screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if buttonBack2._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						menu()
					elif reportButton._rect.collidepoint(event.pos):
						webbrowser.open('https://forms.gle/vrM9PTUPhq4zZdhj6', new=2)

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

if musicChBt.checkbuttonVariable == True:
	pygame.mixer.music.load(os.path.join(musicPath, 'mainTheme.ogg'))
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(0.3)
menu()