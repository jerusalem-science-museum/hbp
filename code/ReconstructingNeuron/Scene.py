import pygame
from pygame.locals import *

from functools import partial

from Button import Button

from pyfribidi import *

LANGUAGE_BUTTONS_X_PADDING = 100
LANGUAGE_BUTTONS_Y_PADDING = 100
LANGUAGE_BUTTONS_SIZE = 100

BACKGROUND_COLOR = [51, 51, 51]
LANGUAGE_TEXT_COLOR = [187, 187, 187]
LANGUAGE_SELECTED_TEXT_COLOR = [249, 207, 71]

BOTTOM_BAR_Y = 999

class Scene:
	def __init__(self, game):
		self.game = game
		self.screen = game.screen
		self.config = game.config

		self.blitCursor = True
		self.backgroundColor = [0,0,0]

		self.logo = pygame.image.load('assets/images/logo.png')
		self.bottomBar = pygame.image.load('assets/images/bottom-bar.png')

		self.buttons = []

		self.backgroundColor = BACKGROUND_COLOR

		self.loadFonts()
		self.createBottomBarButtons()

	def createBottomBarButtons(self):
		homeNormal = pygame.image.load('assets/images/button-home-normal.png')
		homeTapped = pygame.image.load('assets/images/button-home-tapped.png')
		self.buttons.append(Button(self.screen, pygame.Rect(0, BOTTOM_BAR_Y, homeNormal.get_width(), homeNormal.get_height()), 
			homeNormal, homeTapped, None, None, None, None, self.onHomeTapped))

		languagesNum = len(self.config.getLanguages())
		for i in range(languagesNum):
			languageData = self.config.getLanguages()[i]

			languageNormal = pygame.image.load('assets/images/language-button-normal.png')
			languageTapped = pygame.image.load('assets/images/language-button-tapped.png')
			font = pygame.font.Font(languageData['fonts']['textFont']['filename'], languageData['fonts']['textFont']['size'])
			
			self.buttons.append(Button(self.screen, pygame.Rect(self.screen.get_width() - (languagesNum - i) * languageNormal.get_width(), BOTTOM_BAR_Y, 
				languageNormal.get_width(), languageNormal.get_height()), languageNormal, languageTapped, log2vis(languageData['buttonText']), LANGUAGE_TEXT_COLOR, LANGUAGE_SELECTED_TEXT_COLOR, font, partial(self.onLanguageTapped, i)))

	def onHomeTapped(self):
		self.game.gotoHome()

	def onLanguageTapped(self, index):
		self.config.changeLanguage(index)
		self.loadFonts()
		self.onLanguageChanged()

	def loadFonts(self):
		languageData = self.config.getLanguage()
		self.headerFont = pygame.font.Font(languageData['fonts']['headerFont']['filename'], languageData['fonts']['headerFont']['size'])
		self.subHeaderFont = pygame.font.Font(languageData['fonts']['subHeaderFont']['filename'], languageData['fonts']['subHeaderFont']['size'])
		self.textFont = pygame.font.Font(languageData['fonts']['textFont']['filename'], languageData['fonts']['textFont']['size'])
		self.smallTextFont = pygame.font.Font(languageData['fonts']['smallTextFont']['filename'], languageData['fonts']['smallTextFont']['size'])
		self.buttonFont = self.textFont

	def onLanguageChanged(self):
		pass

	def onMouseDown(self, pos):
		for button in self.buttons:
			button.onMouseDown(pos)

	def onMouseUp(self, pos):
		for button in self.buttons:
			button.onMouseUp(pos)

	def draw(self):
		self.screen.blit(self.logo, (23, 17))

		# Draw bottom bar
		self.screen.blit(self.bottomBar, (0, 999))

		# Draw current language image

		for button in self.buttons:
			button.draw()
