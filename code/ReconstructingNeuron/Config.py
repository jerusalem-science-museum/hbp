import json
import pyfribidi

class Config:

	def __init__(self, filename):
		with open(filename) as file:
			self.config = json.load(file)
		self.languagePrefix = self.config['defaultLanguage']
		self.languageIndex = next(index for index in range(len(self.config['languages'])) if self.config['languages'][index]['prefix'] == self.languagePrefix)

	def getText(self, key):
		text = self.config['texts'][self.languagePrefix][key]
		if self.getLanguage()['rtl']:
			text = pyfribidi.log2vis(text)
		return text

	def getTextList(self, key):
		lines = self.config['texts'][self.languagePrefix][key].split('\n')
		if self.getLanguage()['rtl']:
			lines = [pyfribidi.log2vis(s) for s in lines]
		return lines

	def getLanguages(self):
		return self.config['languages']

	def changeLanguage(self, index):
		self.languageIndex = index
		self.languagePrefix = self.getLanguages()[self.languageIndex].languagePrefix

	def getLanguage(self):
		return self.config['languages'][self.languageIndex]

	def isTouch(self):
		return self.config['touch']

	def getTouchDevice(self):
		return self.config['touchDevice']