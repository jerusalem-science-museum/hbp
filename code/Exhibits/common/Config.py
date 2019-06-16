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
		self.languagePrefix = self.getLanguages()[self.languageIndex]['prefix']

	def getLanguage(self):
		return self.config['languages'][self.languageIndex]

	def getDefaultLanguagePrefix(self):
		return self.config['defaultLanguage']

	def isTouch(self):
		return self.config['touch']

	def getTouchDevice(self):
		return self.config['touchDevice']

	def getOpeningVideos(self):
		return self.config['openingVideos']

	def getInstitutions(self, countryKey):
		return self.config['mapCountries'][countryKey]['institutions']

	def getMaxMapDotTapDistance(self):
		return self.config['maxMapDotTapDistance']

	def getCountryName(self, countryKey):
		return self.getText(self.config['mapCountries'][countryKey]['nameKey'])