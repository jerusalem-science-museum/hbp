import pygame
from pygame.locals import *

import cv2
import time
import sys

from common.Exhibit import Exhibit
from common.VideoScene import VideoScene
from common.VideoPlayer import VideoPlayer

from opening.OpeningScene import OpeningScene
from opening.MapScene import MapScene
from opening.CountryScene import CountryScene
from opening.CreditsScene import CreditsScene

EXTRA_CONFIG_FILENAME = 'assets/config/config-opening.json'

class Opening(Exhibit):
	def __init__(self):
		super().__init__()

	def start(self, extraConfigFilename):
		super().start(extraConfigFilename)

		self.preloadVideos()

		self.scene = OpeningScene(self)

		self.loop()

	def preloadVideos(self):
		self.initialVideoFrames = {}

		for video in self.config.getOpeningVideos():
			if video['type'] == 'VIDEO':
				for language in self.config.getLanguages():
					filename = video['file'][language['prefix']]
					self.initialVideoFrames[filename] = VideoPlayer.preloadInitialFrames(filename)

		print(self.config.getInstitutionVideoFilenames())
		for videoFilename in self.config.getInstitutionVideoFilenames():
			for language in self.config.getLanguages():
				filename = 'assets/videos/opening/map/' + videoFilename + '-' + language['prefix'] + '.mp4'
				print(filename)
				self.initialVideoFrames[filename] = VideoPlayer.preloadInitialFrames(filename)

	def gotoHome(self):
		self.scene = OpeningScene(self)

	def transition(self, transitionId, data=None):
		if transitionId == 'VIDEO':
			self.scene = VideoScene(self, data['file'], 'START', data['soundFile'], data.get('hasBack', False), initialFrames=self.initialVideoFrames[data['file']], fps=data['fps'])
		elif transitionId == 'INST_VIDEO':
			self.scene = VideoScene(self, data['file'], 'COUNTRY', data['soundFile'], True, data['countryData'], initialFrames=self.initialVideoFrames[data['file']], fps=data['fps'])
		elif transitionId == 'START':
			self.scene = OpeningScene(self)
		elif transitionId == 'MAP':
			self.scene = MapScene(self)
		elif transitionId == 'COUNTRY':
			self.scene = CountryScene(self, data)
		elif transitionId == 'CREDITS':
			self.scene = CreditsScene(self)

if __name__ == '__main__':
	Opening().start(None if len(sys.argv) == 2 and sys.argv[1] == '--mouse' else EXTRA_CONFIG_FILENAME)