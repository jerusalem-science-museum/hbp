import pygame
from pygame.locals import *

from common.Scene import Scene
from common.Button import Button

from common.Utilities import Utilities

START_BUTTON_TEXT_COLOR = [0, 0, 0]

class LearnMoreScene(Scene):
	def __init__(self, game, evaluation):
		super().__init__(game)

		self.evaluation = evaluation
		self.isHealthy = evaluation['condition']

		self.backButton = Button(self.screen, pygame.Rect(702, 872, 179, 56), 
			pygame.image.load('assets/images/button-small-normal.png'), pygame.image.load('assets/images/button-small-selected.png'), 
			self.config.getText("DFAM_LEARN_MORE_BACK_BUTTON_TEXT"), START_BUTTON_TEXT_COLOR, START_BUTTON_TEXT_COLOR, self.smallButtonTextFont, self.onBackClick)
		self.buttons.append(self.backButton)

		if self.isHealthy:
			self.images = [pygame.image.load("assets/images/doctor/learn-more-mri-healthy.png"), pygame.image.load("assets/images/doctor/learn-more-pet-healthy.png"), pygame.image.load("assets/images/doctor/learn-more-cognitive-healthy.png")]
		else:
			self.images = [pygame.image.load("assets/images/doctor/learn-more-mri-not-healthy.png"), pygame.image.load("assets/images/doctor/learn-more-pet-not-healthy.png"), pygame.image.load("assets/images/doctor/learn-more-cognitive-not-healthy.png")]

		self.imagePositions = [(1321, 159), (1321, 404), (1305, 636)]

		self.createTexts()

	def onBackClick(self):
		self.game.transition('EVALUATE', self.evaluation)

	def onLanguageChanged(self):
		super().onLanguageChanged()
		self.createTexts()
		self.backButton.createText(self.config.getText("DFAM_LEARN_MORE_BACK_BUTTON_TEXT"), self.smallButtonTextFont)

	def createTexts(self):
		self.descTexts = Utilities.renderTextList(self.config, self.smallTextFont, "DFAM_LEARN_MORE_HEALTHY_DESC_TEXT" if self.isHealthy else "DFAM_LEARN_MORE_NOT_HEALTHY_DESC_TEXT")

	def draw(self, dt):
		for i in range(len(self.images)):
			self.screen.blit(self.images[i], self.imagePositions[i])
		Utilities.drawTextsOnCenterX(self.screen, self.descTexts, (791, 152), 40)
		super().draw(dt)