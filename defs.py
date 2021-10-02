import pygame
import os
mainPath = os.path.dirname(__file__)
resourcesPath = os.path.join(mainPath, "resources")
mapsPath = os.path.join(resourcesPath, "maps")

def clip(surf,x,y,x_size,y_size):
	handle_surf = surf.copy()
	clipR = pygame.Rect(x,y,x_size,y_size)
	handle_surf.set_clip(clipR)
	image = surf.subsurface(handle_surf.get_clip())
	return image.copy()

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

def loadMap(path):
	f = open((os.path.join(mapsPath, path)) + '.txt','r')
	data = f.read()
	f.close()
	data = data.split('\n')
	gameMap = []
	for row in data:
		gameMap.append(list(row))
	return gameMap