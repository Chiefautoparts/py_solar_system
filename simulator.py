import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import solarsystem

windowWidth = 1024
windowHeight = 768

pygame.init()
surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)

pygame.display.set_caption('Solar System Simulator')

previousMousePosition = [0,0]
mousePosition = None
mouseDown = False

background = pygame.image.load("assets/background.jpg")
logo = pygame.image.load("assets/logo.png")
UITab = pygame.image.load("assets/tabs.png")
UICoordinates = [{"name": "mercury", "coordinates": (132,687)},
{'name': 'venus', 'coordinates': (229,687)}, 
{'name': 'earth', 'coordinates': (326,687)},
{'name': 'mars', 'coordinates': (423,687)},
{'name': 'jupiter', 'coordinates': (520,687)},
{'name': 'saturn', 'coordinates': (617,687)},
{'name': 'neptune', 'coordinates': (713,687)},
{'name': 'uranus', 'coordinates': (810,687)}]

celestialBodies = []
currentBody = None

drawAttractions = True

gravity = 10.0

def drawUI():
	surface.blit(UITab, (131,687))
	surface.blit(solarsystem.images["mercury"], (158,714))
	surface.blit(solarsystem.images["venus"], (247,706))
	surface.blit(solarsystem.images['earth'], (344,704))
	surface.blit(solarsystem.images['mars'], (451,714))
	surface.blit(solarsystem.images['jupiter'], (524,692))
	surface.blit(solarsystem.images['saturn'], (620,695))
	surface.blit(solarsystem.images['neptune'], (724,697))
	surface.blit(solarsystem.images['uranus'], (822,697))

def drawPlanets():

	for planet in celestialBodies:
		planet["position"][0] += planet["velocity"][0]
		planet["position"][1] += planet["velocity"][1]
		surface.blit(solarsystem.images[planet["name"]], (planet["position"][0] - planet["radius"], planet["position"][1] - planet["radius"]))

def drawCurrentBody():
	currentBody["position"][0] = mousePosition[0]
	currentBody["position"][1] = mousePosition[1]

	surface.blit(solarsystem.images[currentBody["name"]], (currentBody["position"][0] - currentBody["radius"], currentBody["position"][1] - currentBody["radius"]))

def calculateMovement():
	for planet in celestialBodies:
		for otherPlanet in celestialBodies:
			if otherPlanet is not planet:
				direction = (otherPlanet["position"][0] - planet["position"][0], otherPlanet["position"][1] - planet["position"][1])
				magnitude = math.hypot(otherPlanet["position"][0] - planet["position"][0], otherPlanet["position"][1] - planet["position"][1])
				nDirection = (direction[0] / magnitude, direction[1] / magnitude)

				if magnitude < 5:
					magnitude = 5
				elif magnitude > 30:
					magnitude = 30

				strength = ((gravity * planet["mass"] * otherPlanet["mass"]) / (magnitude *magnitude)) / otherPlanet["mass"]

				appliedForce = (nDirection[0] * strength, nDirection[1] * strength)

				otherPlanet["velocity"][0] -= appliedForce[0]

				otherPlanet["velocity"][0] -= appliedForce[0]
				otherPlanet["velocity"][1] -= appliedForce[1]

				if drawAttractions is True:
					pygame.draw.line(surface, (255,255,255),(planet["position"][0],planet["position"][1]),(otherPlanet["position"][0],otherPlanet["position"][1]), 1)

def checkUIForClick(coordinates):
	for tab in UICoordinates:
		tabX = tab["coordinates"][0]

		if coordinates[0] > tabX and coordinates[0] < tabX + 82:
			return tab["name"]

	return False

def handleMouseDown():
	global mousePosition, currentBody

	if(mousePosition[1] >= 687):
		newPlanet = checkUIForClick(mousePosition)

		if newPlanet is not False:
			currentBody = solarsystem.makeNewPlanet(newPlanet)

def quitGame():
	pygame.quit()
	sys.exit()


while True:

	mousePosition = pygame.mouse.get_pos()
	surface.blit(background, (0,0))

	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == pygame.KEYUP:
			
			if event.key == pygame.K_r:
				celestialBodies = []

			if event.key == pygame.K_a:
				if drawAttractions is True:
					drawAttractions = False
				elif drawAttractions is False:
					drawAttractions = True 

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
			handleMouseDown()

		if event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	drawUI()
	calculateMovement()
	drawPlanets()

	if currentBody is not None:
		drawCurrentBody()

		if mouseDown is False:
			currentBody["velocity"][0] = (mousePosition[0] - previousMousePosition[0]) / 4 
			currentBody["velocity"][1] = (mousePosition[1] - previousMousePosition[1]) / 4
			celestialBodies.append(currentBody)
			currentBody = None

	if GAME_TIME.get_ticks() < 4000:
		surface.blit(logo, (108,77))

	previousMousePosition = mousePosition

	pygame.display.update()