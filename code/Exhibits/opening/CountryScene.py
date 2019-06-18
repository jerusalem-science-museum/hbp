import pygame
from pygame.locals import *

from functools import partial
import math

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class CountryScene(Scene):
	def __init__(self, game, countryKey):
		super().__init__(game)

		self.countryKey = countryKey

		self.countryImage = pygame.image.load('assets/images/opening/map/' + countryKey + '-big.png')
		self.countryImagePos = (601 - self.countryImage.get_width() // 2, 548 - self.countryImage.get_height() // 2)
		self.dotImage = pygame.image.load('assets/images/opening/map/dot-normal.png')
		self.selectedDotImage = pygame.image.load('assets/images/opening/map/dot-selected.png')

		self.institutions = self.config.getInstitutions(self.countryKey)
		self.institutionIndex = None

		self.createTexts()

	def onCountryClick(self, countryKey):
		self.map.transition('COUNTRY', countryKey)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.loadInstitution()

	def createTexts(self):
		self.countryHeader = self.headerFont.render(self.config.getCountryName(self.countryKey), True, (249, 207, 71))
		self.tapInstructions = self.smallTextFont.render(self.config.getText("OS_MAP_SELECT_DOT_INSTRUCTIONS"), True, (255, 255, 255))

	def onMouseDown(self, pos):
		super().onMouseDown(pos)
		self.tappedIndex = self.getClosestDotIndex(pos)

	def onMouseUp(self, pos):
		super().onMouseUp(pos)
		releaseIndex = self.getClosestDotIndex(pos)
		if self.tappedIndex is not None and self.tappedIndex == releaseIndex:
			self.selectIndex(self.tappedIndex)
		self.tappedIndex = None

	def getClosestDotIndex(self, pos):
		closestIndex = None
		closestDist = self.config.getMaxMapDotTapDistance()
		for i in range(len(self.institutions)):
			institution = self.institutions[i]
			dotCenterPosition = (self.countryImagePos[0] + institution['mapX'], self.countryImagePos[1] + institution['mapY'])
			dist = math.hypot(dotCenterPosition[0] - pos[0], dotCenterPosition[1] - pos[1])
			if dist < self.config.getMaxMapDotTapDistance():
				if dist < closestDist:
					closestIndex = i
					closestDist = dist

		return closestIndex

	def selectIndex(self, index):
		self.institutionIndex = index
		self.loadInstitution()

	def loadInstitution(self):
		institution = self.institutions[self.institutionIndex]
		self.institutionHeader = Utilities.renderTextList(self.config, self.subHeaderFont, institution['nameKey'], (255, 255, 255))
		self.institutionCity = Utilities.renderTextList(self.config, self.subHeaderFont, institution['cityKey'], (255, 255, 255))
		self.institutionDesc = Utilities.renderTextList(self.config, self.subHeaderFont, institution['descriptionKey'], (255, 255, 255))
		self.institutionImage = pygame.image.load('assets/images/opening/map/institutions/spain-test.png')

		self.institutionHeaderY = 579
		self.institutionCityY = 627
		self.institutionDescY = 684

	def draw(self, dt):
		self.screen.blit(self.countryImage, self.countryImagePos)
		for i in range(0, len(self.institutions)):
			institution = self.institutions[i]
			dotCenterPosition = (self.countryImagePos[0] + institution['mapX'], self.countryImagePos[1] + institution['mapY'])
			if self.institutionIndex == i:
				self.screen.blit(self.selectedDotImage, (dotCenterPosition[0] - self.selectedDotImage.get_width() // 2, dotCenterPosition[1] - self.selectedDotImage.get_height() // 2))
			else:
				self.screen.blit(self.dotImage, (dotCenterPosition[0] - self.dotImage.get_width() // 2, dotCenterPosition[1] - self.dotImage.get_height() // 2))

		if self.institutionIndex is None:
			Utilities.drawTextOnCenterX(self.screen, self.countryHeader, (1098 + self.countryHeader.get_width() // 2, 402))
			Utilities.drawTextOnCenterX(self.screen, self.tapInstructions, (1098 + self.tapInstructions.get_width() // 2, 580))
		else:
			self.screen.blit(self.institutionImage, (1093, 219))
			Utilities.drawTextsOnLeftX(self.screen, self.institutionHeader, (1093 ,self.institutionHeaderY), 30)
			Utilities.drawTextsOnLeftX(self.screen, self.institutionCity, (1093 ,self.institutionCityY), 30)
			Utilities.drawTextsOnLeftX(self.screen, self.institutionDesc, (1093 ,self.institutionDescY), 30)

		super().draw(dt)