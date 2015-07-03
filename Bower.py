from . import Base
import os
import sublime

## ===========================================
## ================ Bower ====================
## ===========================================
## Docs: http://bower.io/docs/api/
## ===========================================

class BowerCommand(Base.BaseCommand):

	def getModuleBaseCommand(self):
		return "bower --no-color"

	def getInstalledPackages(self):
		bowerFile = self.getProjectPath() + "/bower.json"

		content = self.file_get_contents(bowerFile)

		bower = sublime.decode_value(content)
		dependencies = bower['dependencies']

		installedPackages = []

		for key in dependencies:
			installedPackages.append(key)

		return installedPackages

	def is_visible(self):
		return self.projectFileExists("bower.json")

class BowerInputCommand(Base.InputCommand):

	def getModuleBaseCommand(self):
		return "bower --no-color"

	def process(self, name):
		command = self.getComponent() + " " + name + " --save"
		
		self.startCommand(command)

	def is_visible(self):
		return self.projectFileExists("bower.json")

## ================ Install ====================

class BowerInstallDependenciesCommand(BowerCommand):

	def process(self):
		self.startCommand("install")

class BowerInstallCommand(BowerCommand):

	_bowerComponents = None

	def process(self):
		self.getBowerPackages()
		self.window.show_quick_panel(self._bowerComponents, self.packageSelected)

	def packageSelected(self, index):
		if (index == -1):
			return

		name = self._bowerComponents[index][0]

		self.startCommand("install " + name + " --save")

	def getBowerPackages(self):
		if (self._bowerComponents is not None):
			return
			
		cacheFile = self.getCachePath() + "\\bower-component-list.json"

		if not os.path.isfile(cacheFile):
			apiUrl = 'https://bower-component-list.herokuapp.com'

			## TODO: do it async
			urllib.request.urlretrieve(apiUrl, cacheFile)
		
		content = self.file_get_contents(cacheFile)

		self._bowerComponents = []

		for idx, val in enumerate(sublime.decode_value(content)):

			name = val.get('name')
			desc = val.get('description', "Description not provided")
			updated = val.get('updated', "Last updated not provided")
			stars = 0 if not val['stars'] else val['stars']

			if ((not name) or (not desc) or (not updated) or stars < 1):
				continue

			component = [name, desc, updated]

			self._bowerComponents.append(component)

class BowerInstallByNameCommand(BowerInputCommand):

	def getMessage(self):
		return "Bower package name:"

	def getComponent(self):
		return "install"

## ================ Update ====================
class BowerUpdateDependenciesCommand(BowerCommand):

	def process(self):
		self.startCommand("update")

class BowerUpdateCommand(BowerCommand):

	def process(self):
		self._bowerComponents = self.getInstalledPackages()
		self.window.show_quick_panel(self._bowerComponents, self.packageSelected)

	def packageSelected(self, index):
		if (index == -1):
			return

		name = self._bowerComponents[index]

		self.startCommand("update " + name)


## ================ Uninstall ====================
class BowerUninstallCommand(BowerCommand):

	def process(self):
		self._bowerComponents = self.getInstalledPackages()
		self.window.show_quick_panel(self._bowerComponents, self.packageSelected)

	def packageSelected(self, index):
		if (index == -1):
			return

		name = self._bowerComponents[index]

		self.startCommand("uninstall " + name + " --save")
