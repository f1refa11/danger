import pygame
import json
config = {
	# "level": 1,
	# "music": True,
	# "sfx": True,
	# "showFPS": False,
	# "fullscreen": False,
 	# "activatedTexturePack": "Default",
	# "language": "ru"
}
# with open("config.json", "w") as f:
#     json.dump(config, f)
with open("config.json") as f:
	config = json.load(f)
activatedTexturePacks = [False, False, False]

while 1:
	pygame.init()
	joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
	pygame.mouse.set_visible(False)
	import os
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 30)
	mainPath = os.path.dirname(__file__)
	resourcesPath = os.path.join(mainPath, "resources")
	windowSize = (896, 640)
	pygame.display.set_caption('Danger!')
	if config["fullscreen"] == True:
		screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN)
	else:
		screen = pygame.display.set_mode(windowSize)
	display = pygame.Surface((448, 320))
	imagesPath = os.path.join(resourcesPath, "textures")
	activeTextures = os.path.join(imagesPath, config["activatedTexturePack"])
	musicPath = os.path.join(resourcesPath, "music")
	soundsPath = os.path.join(resourcesPath, "sounds")
	texturePacks = os.listdir(imagesPath)
	temp = ""

	if len(texturePacks) == 2:
		if texturePacks[1] == "Default":
			temp = texturePacks[0]
			texturePacks[0] = texturePacks[1]
			texturePacks[1] = temp
		if config["activatedTexturePack"] == texturePacks[0]:
			activatedTexturePacks = [True, False]
		else:
			activatedTexturePacks = [False, True]
	elif len(texturePacks) == 3:
		if texturePacks[2] == "Default":
			temp = texturePacks[0]
			texturePacks[0] = texturePacks[2]
			texturePacks[2] = temp
		if config["activatedTexturePack"] == texturePacks[0]:
			activatedTexturePacks = [True, False, False]
		if config["activatedTexturePack"] == texturePacks[1]:
			activatedTexturePacks = [False, True, False]
		else:
			activatedTexturePacks = [False, False, True]
	
	#loading images
	logoImg = pygame.image.load(os.path.join(activeTextures, 'logo.png')).convert_alpha()
	backgroundImg = pygame.image.load(os.path.join(activeTextures, 'bg.png')).convert()
	gameBackgroundImg = pygame.image.load(os.path.join(activeTextures, "bg2.png")).convert()
	loadingScreenImg = pygame.image.load(os.path.join(activeTextures, "loading.png")).convert()
	vignetteImg = pygame.image.load(os.path.join(activeTextures, "vignette.png")).convert_alpha()
	background = pygame.transform.scale(backgroundImg, (backgroundImg.get_width()*8, backgroundImg.get_height()*8))
	gameBackground = pygame.transform.scale(gameBackgroundImg, (gameBackgroundImg.get_width()*8, gameBackgroundImg.get_height()*8))
	loadingScreen = pygame.transform.scale(loadingScreenImg, (loadingScreenImg.get_width()*8, loadingScreenImg.get_height()*8))
	vignette = pygame.transform.scale(vignetteImg, (vignetteImg.get_width()*4, vignetteImg.get_height()*4))
	grassImg = pygame.image.load(os.path.join(activeTextures, 'grass.png')).convert()
	dirtImg = pygame.image.load(os.path.join(activeTextures, 'dirt.png')).convert()
	playerRightImg = pygame.image.load(os.path.join(activeTextures, 'playerRight.png')).convert_alpha()
	playerLeftImg = pygame.image.load(os.path.join(activeTextures, "playerLeft.png")).convert_alpha()
	playerJumpImg = pygame.image.load(os.path.join(activeTextures, 'playerJump.png')).convert_alpha()
	playerImg = playerRightImg
	stoneImg = pygame.image.load(os.path.join(activeTextures, 'stone.png')).convert()
	spikeImg = pygame.image.load(os.path.join(activeTextures, 'spikes.png')).convert_alpha()
	finishFlagImg = pygame.image.load(os.path.join(activeTextures, 'finish-flag.png')).convert_alpha()
	checkpointFlagImg = pygame.image.load(os.path.join(activeTextures, 'checkpoint-flag.png')).convert_alpha()
	bridgeLeftImg = pygame.image.load(os.path.join(activeTextures, 'bridge-left.png'))
	bridgeRightImg = pygame.image.load(os.path.join(activeTextures, 'bridge-right.png'))
	bridgeCenterImg = pygame.image.load(os.path.join(activeTextures, 'bridge-center.png'))
	checkbuttonEmpty = pygame.image.load(os.path.join(activeTextures, 'checkbutton_empty.png')).convert_alpha()
	checkbuttonChecked = pygame.image.load(os.path.join(activeTextures, 'checkbutton_checked.png')).convert_alpha()
	gameMenuImg = pygame.image.load(os.path.join(activeTextures, 'gameMenuUI.png')).convert_alpha()
	cursorImg = pygame.image.load(os.path.join(activeTextures, 'cursor.png')).convert_alpha()
	screen.blit(loadingScreen, (0,0))
	pygame.display.update()
	from pygame.locals import *
	import sys
	import time
	import random
	from defs import *
	from Font import *
	import json
	import time
	import random
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
gameMenuActivated = False
f3Menu = False
if config["language"] == "ru":
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

clock = pygame.time.Clock()

beepSound = pygame.mixer.Sound(os.path.join(soundsPath, 'beep.wav'))

#resizing loaded images
cursor = pygame.transform.scale(cursorImg, (cursorImg.get_width()*2, cursorImg.get_height()*2))

pygame.display.set_icon(playerJumpImg)

#player collision rect
playerRect = pygame.Rect(56,16,8,16)

lastTime = time.time()

#Functions/Classes
def clip(surf,x,y,x_size,y_size):
	handle_surf = surf.copy()
	clipR = pygame.Rect(x,y,x_size,y_size)
	handle_surf.set_clip(clipR)
	image = surf.subsurface(handle_surf.get_clip())
	return image.copy()

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
		self.source = pygame.image.load(os.path.join(activeTextures, 'button.png')).convert_alpha()
		self.pressed = pygame.image.load(os.path.join(activeTextures, "buttonPressed.png")).convert_alpha()
		self.hovered = pygame.image.load(os.path.join(activeTextures, "buttonHover.png")).convert_alpha()
		self.texture = pygame.transform.scale(self.source, (self.source.get_width()*3, self.source.get_height()*3))
		self.texturePressed = pygame.transform.scale(self.pressed, (self.pressed.get_width()*3, self.pressed.get_height()*3))
		self.textureHovered = pygame.transform.scale(self.hovered, (self.hovered.get_width()*3, self.hovered.get_height()*3))
		self.buttonText = buttonText
		self.buttonX = buttonX
		self.buttonY = buttonY
		self._rect = pygame.Rect(buttonX, buttonY, self.texture.get_width(), self.texture.get_height())
		self.buttonState = "main"
	def draw(self, screen):
		if self.buttonState == "main":
			screen.blit(self.texture, self._rect)
			gameFont.render(screen, self.buttonText, (self.buttonX*1.25, self.buttonY+20))
		elif self.buttonState == "pressed":
			screen.blit(self.texturePressed, self._rect)
			gameFont.render(screen, self.buttonText, (self.buttonX*1.35, self.buttonY+20))
		elif self.buttonState == "hovered":
			screen.blit(self.textureHovered, self._rect)
			gameFont.render(screen, self.buttonText, (self.buttonX*1.25, self.buttonY+20))

class CheckButton(object):
	def __init__(self, checkbuttonX, checkbuttonY, checkbuttonVariable):
		self.checkbuttonEmpty = pygame.image.load(os.path.join(activeTextures, 'checkbutton_empty.png'))
		self.checkbuttonChecked = pygame.image.load(os.path.join(activeTextures, 'checkbutton_checked.png'))
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
		self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',"А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь","э", "ю", "я",".","-",',',':','+',"'",'!','?','0','1','2','3','4','5','6','7','8','9']
		font_img_org = pygame.image.load(path)
		font_img = pygame.transform.scale(font_img_org, (font_img_org.get_width()*2, font_img_org.get_height()*2))
		current_char_width = 0
		self.characters = {}
		character_count = 0
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
bigFont = Font(os.path.join(activeTextures, 'bigFont.png'))
gameFont = Font(os.path.join(activeTextures, 'font.png'))
grayFont = Font(os.path.join(activeTextures, 'grayFont.png'))

player = Player(100, 48, speed)

#menu buttons
buttonPlay = Button(448-40, 150, lang[0])
buttonSettings = Button(448-40, 250, lang[1])
buttonAbout = Button(448-40, 350, lang[2])
exitGame = Button(448-40, 450, lang[3])

#settings buttons
langSettingsButton = Button(170, 150, lang[16])
viewSettingsButton = Button(450, 150, lang[15])
soundSettingsButton = Button(170, 250, lang[17])
musicChBt = CheckButton(550, 150, config["music"])
sfxChBt = CheckButton(550, 250, config["sfx"])
showFPSChBt = CheckButton(550, 150, config["showFPS"])
fullscreeenChBt = CheckButton(550, 250, config["fullscreen"])
customTexturesSettingsButton = Button(450, 250, "Textures")
buttonBack = Button(350, 550, lang[4])

if len(activatedTexturePacks) == 1:
	activateTexturePack1 = CheckButton(550,150, activatedTexturePacks[0])
elif len(activatedTexturePacks) == 2:
	activateTexturePack1 = CheckButton(550,150, activatedTexturePacks[0])
	activateTexturePack2 = CheckButton(550,250, activatedTexturePacks[1])
elif len(activatedTexturePacks) == 3:
	activateTexturePack1 = CheckButton(550,150, activatedTexturePacks[0])
	activateTexturePack2 = CheckButton(550,250, activatedTexturePacks[1])
	activateTexturePack3 = CheckButton(550,350, activatedTexturePacks[2])

#gameMenu buttons
resumeGame = Button(448-40, 100, lang[5])
saveGame = Button(448-40, 200, lang[6])
settingsGameMenu = Button(448-40, 300, lang[1])
exitFromGame = Button(448-40, 400, lang[3])

#selectMode buttons
newGame = Button(350, 100, lang[7])
loadGame = Button(350, 200, lang[8])

#createGame buttons
createLevelsMode = Button(448-40, 100, lang[9])

buttonBack2 = Button(350, 500, lang[4])

reportButton = Button(350, 400, lang[27])

def levelsMode(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerLeftImg, playerRightImg, gameMenuActivated, f3Menu, checkpointed):
	global playerImg, checkpointPosition
	while 1:

		display.blit(gameBackground, (0,0))

		trueScroll[0] += (playerRect.x-trueScroll[0]-202)/25
		trueScroll[1] += (playerRect.y-trueScroll[1]-146)/20
		scroll = trueScroll.copy()
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])

		
		tileRects = []
		spike_rects = []
		finish_flag_rects = []
		checkpoint_flag_rects = []
		y = 0
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
			playerImg = pygame.image.load(os.path.join(activeTextures, 'playerRight.png'))
		if player.moveLeft == True:
			playerMovement[0] -= speed
			playerImg = pygame.image.load(os.path.join(activeTextures, 'playerLeft.png'))
		playerMovement[1] += player.jumpCount
		player.jumpCount += 0.2
		if jumpCount > 3:
			jumpCount = 3

		playerRect,collisions = move(playerRect,playerMovement,tileRects)

		if collisions['bottom'] == True:
			# playerImg = pygame.image.load(os.path.join(activeTextures, 'player.png'))
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
				checkpointed = False
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
							pygame.mixer.Channel(0).set_volume(0.3)
							if random.randint(0,1) == 0:
								pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jumpVariant1.wav')))
							else:
								pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, "jumpVariant2.wav")))
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
							pygame.mixer.Channel(0).set_volume(0.3)
							if random.randint(0,1) == 0:
								pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jumpVariant1.wav')))
							else:
								pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, "jumpVariant2.wav")))
						player.jumpCount = -5
				if event.key == K_w:
					if player.airTimer < 6:
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(0).set_volume(0.3)
							if random.randint(0,1) == 0:
								pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, 'jumpVariant1.wav')))
							else:
								pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(soundsPath, "jumpVariant2.wav")))
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
						settings()
					elif saveGame._rect.collidepoint(event.pos):
						pass

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

		screen.blit(pygame.transform.scale(display,windowSize),(0,0))
		player.draw(display)
		screen.blit(vignette, (0,0))
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

def menu():
	while 1:

		screen.blit(background, (0,0))

		buttonPlay.draw(screen)
		buttonSettings.draw(screen)
		buttonAbout.draw(screen)
		exitGame.draw(screen)

		mousePosition = pygame.mouse.get_pos()

		gameFont.render(screen, "0.4.5", (0, 616))

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
						settings()
					elif buttonAbout._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						about()
					elif exitGame._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						sys.exit()

		if buttonPlay._rect.collidepoint(mousePosition):
			buttonPlay.buttonState = "hovered"
		else:
			buttonPlay.buttonState = "main"

		if buttonSettings._rect.collidepoint(mousePosition):
			buttonSettings.buttonState = "hovered"
		else:
			buttonSettings.buttonState = "main"

		if buttonAbout._rect.collidepoint(mousePosition):
			buttonAbout.buttonState = "hovered"
		else:
			buttonAbout.buttonState = "main"
		
		if exitGame._rect.collidepoint(mousePosition):
			exitGame.buttonState = "hovered"
		else:
			exitGame.buttonState = "main"

		screen.blit(logoImg, (315, 5))
		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def settings():
	while 1:
		screen.blit(background, (0,0))

		bigFont.render(screen, lang[1], (330, 50))

		buttonBack.draw(screen)
		langSettingsButton.draw(screen)
		soundSettingsButton.draw(screen)
		viewSettingsButton.draw(screen)
		customTexturesSettingsButton.draw(screen)

		mousePosition = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if langSettingsButton._rect.collidepoint(event.pos):
						langSettings()
					elif soundSettingsButton._rect.collidepoint(event.pos):
						soundSettings()
					elif viewSettingsButton._rect.collidepoint(event.pos):
						viewSettings(screen)
					elif customTexturesSettingsButton._rect.collidepoint(event.pos):
						texturesSettings()
					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						menu()

		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"

		if langSettingsButton._rect.collidepoint(mousePosition):
			langSettingsButton.buttonState = "hovered"
		else:
			langSettingsButton.buttonState = "main"

		if soundSettingsButton._rect.collidepoint(mousePosition):
			soundSettingsButton.buttonState = "hovered"
		else:
			soundSettingsButton.buttonState = "main"

		if viewSettingsButton._rect.collidepoint(mousePosition):
			viewSettingsButton.buttonState = "hovered"
		else:
			viewSettingsButton.buttonState = "main"

		if customTexturesSettingsButton._rect.collidepoint(mousePosition):
			customTexturesSettingsButton.buttonState = "hovered"
		else:
			customTexturesSettingsButton.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def viewSettings(screen):
	while 1:
		screen.blit(background, (0,0))

		bigFont.render(screen, lang[15], (330, 50))
		bigFont.render(screen, lang[18], (150, 150))
		bigFont.render(screen, lang[19], (150, 250))

		buttonBack.draw(screen)
		showFPSChBt.draw(screen)
		fullscreeenChBt.draw(screen)

		mousePosition = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if showFPSChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if config["showFPS"] == True:
							config["showFPS"] = False
							showFPSChBt.checkbuttonVariable = config["showFPS"]
						else:
							config["showFPS"] = True
							showFPSChBt.checkbuttonVariable = config["showFPS"]

					elif fullscreeenChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if config["fullscreen"] == True:
							config["fullscreen"] = False
							fullscreeenChBt.checkbuttonVariable = config["fullscreen"]
							screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
						else:
							config["fullscreen"] = True
							fullscreeenChBt.checkbuttonVariable = config["fullscreen"]
							screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.FULLSCREEN)

					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						settings()

				with open("config.json", "w") as f:
					json.dump(config, f)
		
		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"
		
		if showFPSChBt._rect.collidepoint(mousePosition):
			showFPSChBt.buttonState = "hovered"
		else:
			showFPSChBt.buttonState = "main"

		if fullscreeenChBt._rect.collidepoint(mousePosition):
			fullscreeenChBt.buttonState = "hovered"
		else:
			fullscreeenChBt.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def soundSettings():
	while 1:
		screen.blit(background, (0,0))

		bigFont.render(screen, lang[17], (330, 50))
		bigFont.render(screen, lang[13], (280, 150))
		bigFont.render(screen, lang[14], (280, 250))

		buttonBack.draw(screen)
		musicChBt.draw(screen)
		sfxChBt.draw(screen)

		mousePosition = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if musicChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if config["music"] == True:
							config["music"] = False
							musicChBt.checkbuttonVariable = config["music"]
						else:
							config["music"] = True
							musicChBt.checkbuttonVariable = config["music"]

					elif sfxChBt._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if config["sfx"] == True:
							config["sfx"] = False
							sfxChBt.checkbuttonVariable = config["sfx"]
						else:
							config["sfx"] = True
							sfxChBt.checkbuttonVariable = config["sfx"]

					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						settings()

					with open("config.json", "w") as f:
					    json.dump(config, f)

		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"

		if musicChBt._rect.collidepoint(mousePosition):
			musicChBt.buttonState = "hovered"
		else:
			musicChBt.buttonState = "main"

		if sfxChBt._rect.collidepoint(mousePosition):
			sfxChBt.buttonState = "hovered"
		else:
			sfxChBt.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def langSettings():
	while 1:
		screen.blit(background, (0,0))

		bigFont.render(screen, lang[16], (330, 50))
		engRect = pygame.Rect(330, 150, 162, 64)
		ruRect = pygame.Rect(330, 220, 162, 64)

		buttonBack.draw(screen)

		mousePosition = pygame.mouse.get_pos()

		if config["language"] == "en":
			bigFont.render(screen, "English", (330, 150))
		else:
			grayFont.render(screen, "English", (330, 150))
		if config["language"] == "ru":
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
					if sfxChBt.checkbuttonVariable == True:
						pygame.mixer.Channel(4).play(beepSound)
					if engRect.collidepoint(event.pos):
						config["language"] = "en"
					elif ruRect.collidepoint(event.pos):
						config["language"] = "ru"
					elif buttonBack._rect.collidepoint(event.pos):
						settings()

					with open("config.json", "w") as f:
					    json.dump(config, f)

		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def texturesSettings():
	global activateTexturePack2, activateTexturePack1, activateTexturePack3
	if len(activatedTexturePacks) == 1:
		activateTexturePack2 = CheckButton(550,250, activatedTexturePacks[0])
	if len(activatedTexturePacks) == 2:
		activateTexturePack2 = CheckButton(550,250, activatedTexturePacks[1])
	if len(activatedTexturePacks) == 3:
		activateTexturePack3 = CheckButton(550,350, activatedTexturePacks[2])
	while 1:
		screen.blit(background, (0,0))

		bigFont.render(screen, "Custom Textures", (260,50))
		if len(texturePacks) == 1:
			bigFont.render(screen, texturePacks[0], (280, 150))
			activateTexturePack1.draw(screen)
		if len(texturePacks) == 2:
			bigFont.render(screen, texturePacks[0], (280, 150))
			bigFont.render(screen, texturePacks[1], (280, 250))
			activateTexturePack1.draw(screen)
			activateTexturePack2.draw(screen)
		elif len(texturePacks) == 3:
			bigFont.render(screen, texturePacks[0], (280, 150))
			bigFont.render(screen, texturePacks[1], (280, 250))
			bigFont.render(screen, texturePacks[2], (280, 350))
			activateTexturePack1.draw(screen)
			activateTexturePack2.draw(screen)
			activateTexturePack3.draw(screen)

		buttonBack.draw(screen)

		mousePosition = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if sfxChBt.checkbuttonVariable == True:
						pygame.mixer.Channel(4).play(beepSound)
					if activateTexturePack1._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						if activatedTexturePacks[0] == False:
							if len(activatedTexturePacks) == 1:
								activatedTexturePacks[0] = True
								activatedTexturePacks[1] = False
								activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
							if len(activatedTexturePacks) == 2:
								activatedTexturePacks[0] = True
								activatedTexturePacks[1] = False
								activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
								activateTexturePack2.checkbuttonVariable = activatedTexturePacks[1]
							elif len(activatedTexturePacks) == 3:
								activatedTexturePacks[0] = True
								activatedTexturePacks[1] = False
								activatedTexturePacks[2] = False
								activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
								activateTexturePack2.checkbuttonVariable = activatedTexturePacks[1]
								activateTexturePack3.checkbuttonVariable = activatedTexturePacks[2]
							activatedTexturePacks[0] = True
							activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
							config["activatedTexturePack"] = texturePacks[0]
					
					if len(activatedTexturePacks) == 2:
						if activateTexturePack2._rect.collidepoint(event.pos):
							if sfxChBt.checkbuttonVariable == True:
								pygame.mixer.Channel(4).play(beepSound)
							if activatedTexturePacks[1] == False:
								if len(activatedTexturePacks) == 2:
									activatedTexturePacks[0] = False
									activatedTexturePacks[1] = True
									activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
									activateTexturePack2.checkbuttonVariable = activatedTexturePacks[1]
								elif len(activatedTexturePacks) == 3:
									activatedTexturePacks[0] = False
									activatedTexturePacks[1] = True
									activatedTexturePacks[2] = False
									activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
									activateTexturePack2.checkbuttonVariable = activatedTexturePacks[1]
									activateTexturePack3.checkbuttonVariable = activatedTexturePacks[2]
								activatedTexturePacks[0] = False
								activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
								config["activatedTexturePack"] = texturePacks[1]
					
					if len(activatedTexturePacks) == 3:
						if activateTexturePack3._rect.collidepoint(event.pos):
							if sfxChBt.checkbuttonVariable == True:
								pygame.mixer.Channel(4).play(beepSound)
							if activatedTexturePacks[2] == False:
								if len(activatedTexturePacks) == 2:
									activatedTexturePacks[0] = False
									activatedTexturePacks[1] = False
									activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
									activateTexturePack2.checkbuttonVariable = activatedTexturePacks[1]
								elif len(activatedTexturePacks) == 3:
									activatedTexturePacks[0] = False
									activatedTexturePacks[1] = False
									activatedTexturePacks[2] = True
									activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
									activateTexturePack2.checkbuttonVariable = activatedTexturePacks[1]
									activateTexturePack3.checkbuttonVariable = activatedTexturePacks[2]
								activatedTexturePacks[0] = False
								activateTexturePack1.checkbuttonVariable = activatedTexturePacks[0]
								config["activatedTexturePack"] = texturePacks[2]

				with open("config.json", "w") as f:
					json.dump(config, f)
				
		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def selectMode():
	while 1:
		screen.blit(background, (0,0))

		newGame.draw(screen)
		loadGame.draw(screen)
		buttonBack.draw(screen)

		mousePosition = pygame.mouse.get_pos()

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
						level = int(config["level"])
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
						levelsMode(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerLeftImg, playerRightImg, gameMenuActivated, f3Menu, checkpointed)
					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						menu()

		if newGame._rect.collidepoint(mousePosition):
			newGame.buttonState = "hovered"
		else:
			newGame.buttonState = "main"

		if loadGame._rect.collidepoint(mousePosition):
			loadGame.buttonState = "hovered"
		else:
			loadGame.buttonState = "main"

		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def createGame():
	while 1:
		screen.blit(background, (0,0))

		createLevelsMode.draw(screen)
		buttonBack.draw(screen)

		mousePosition = pygame.mouse.get_pos()

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
						levelsMode(playerRect, moveRight, moveLeft, jumpCount, airTimer, fails, gameMap, level, playerLeftImg, playerRightImg, gameMenuActivated, f3Menu, checkpointed)
					elif buttonBack._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						selectMode()

		if createLevelsMode._rect.collidepoint(mousePosition):
			createLevelsMode.buttonState = "hovered"
		else:
			createLevelsMode.buttonState = "main"

		if buttonBack._rect.collidepoint(mousePosition):
			buttonBack.buttonState = "hovered"
		else:
			buttonBack.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

def about():
	while 1:
		screen.blit(background, (0,0))

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

		mousePosition = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if buttonBack2._rect.collidepoint(event.pos):
						if sfxChBt.checkbuttonVariable == True:
							pygame.mixer.Channel(4).play(beepSound)
						menu()

		if buttonBack2._rect.collidepoint(mousePosition):
			buttonBack2.buttonState = "hovered"
		else:
			buttonBack2.buttonState = "main"

		if reportButton._rect.collidepoint(mousePosition):
			reportButton.buttonState = "hovered"
		else:
			reportButton.buttonState = "main"

		screen.blit(cursor, pygame.mouse.get_pos())
		pygame.display.update()
		clock.tick(60)

if musicChBt.checkbuttonVariable == True:
	pygame.mixer.music.load(os.path.join(musicPath, 'mainTheme.ogg'))
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(0.3)
menu()