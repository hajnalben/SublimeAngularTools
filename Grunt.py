import sublime, sublime_plugin
import subprocess, os, getpass, signal
import urllib.request
from threading import Thread

userName = getpass.getuser()
osType = os.name
separator = '&' if osType == 'nt' else ';'

## ===========================================
## ================ Base =====================
## ===========================================

class BaseCommand(sublime_plugin.WindowCommand):

	def getProjectPath(self):
		return self.window.extract_variables()['project_path']

	def getCachePath(self):
		return sublime.cache_path()

	def run(self):
		self.process()

	# Utility functions

	def startAsync(self, callback, args):
		thread = Thread(target = callback, args = args)
		thread.start()

	def startCommand(self, command):
		self.startAsync(self.sub_process_cmd, [command])

	_process = None

	def sub_process_cmd(self, command):
		print("Running command: " + command)

		if (osType is not 'nt'):
			command = 'export PATH=/usr/local/bin/:$PATH ;' + command

		self._process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		self._process.wait()

		print("Finished")

		sublime.status_message("Command finished!")

		print(self._process.stderr.readline())

		line = self._process.stdout.readline()

		while self._process is not None:
			if not line:
				break

			print(line)

			line = self._process.stdout.readline()

class InputCommand(BaseCommand):

	def getDefaultValue(self):
		return ""

	def run(self):
		self.window.show_input_panel(self.getMessage(), self.getDefaultValue(), self.preProcess, None, None)

	def preProcess(self, name):
		if not name:
			print("Name is empty! Stopping...")
			return

		self.process(name)

## ===========================================
## ================ Bower ====================
## ===========================================

class BowerCommand(BaseCommand):

	def getMessage(self):
		return "Component name:"

	def getBaseCommand(self):
		return "cd " + self.getProjectPath() + " " + separator + " bower "

	def file_get_contents(self, filename):
		with open(filename, encoding="utf8") as f:
			return f.read()

class BowerInstallCommand(BowerCommand):

	_bowerComponents = None

	def process(self):

		if (self._bowerComponents is None):
			apiUrl = 'https://bower-component-list.herokuapp.com'

			cacheFile = self.getCachePath() + "\\bower-component-list.json"

			if not os.path.isfile(cacheFile):
				## Másik szálon kellene
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

		self.window.show_quick_panel(self._bowerComponents, self.packageSelected)

	def packageSelected(self, index):
		if (index == -1):
			return

		name = self._bowerComponents[index][0]
		self.startCommand(self.getBaseCommand() + "install " + name + " --save")

class BowerUninstallCommand(BowerCommand):

	_bowerComponents = None

	def process(self):

		bowerFile = self.getProjectPath() + "/bower.json"

		content = self.file_get_contents(bowerFile)

		bower = sublime.decode_value(content)
		dependencies = bower['dependencies']

		self._bowerComponents = []

		for key in dependencies:
			self._bowerComponents.append(key)

		self.window.show_quick_panel(self._bowerComponents, self.packageSelected)

	def packageSelected(self, index):
		if (index == -1):
			return

		name = self._bowerComponents[index]

		self.startCommand(self.getBaseCommand() + "uninstall " + name + " --save")

## ===========================================
## ================ Grunt ====================
## ===========================================

class GruntCommand(BaseCommand):

	def getBaseCommand(self):
		return "cd " + self.getProjectPath() + " " + separator + " grunt --no-color "
		
	def process(self):
		self.startCommand(self.getBaseCommand())


class GruntServeCommand(GruntCommand):
	
	def process(self):

		if self._process is None:
			print("start")
			self.startCommand(self.getBaseCommand() + "serve")
		else:
			print("stop")
			print(self._process.pid)
			##self._process.send_signal(signal.CTRL_C_EVENT)
			##os.kill(self._process.pid, signal.CTRL_C_EVENT)
			self._process.terminate()
			self._process = None

class GruntTestCommand(GruntCommand):

	def process(self):
		self.startCommand(self.getBaseCommand() + "test")

class GruntBuildCommand(GruntCommand):

	def process(self):
		self.startCommand(self.getBaseCommand() + "build")

## ===========================================
## ================ Yeomann ==================
## ===========================================

class YoCommand(InputCommand):

	def process(self, name):
		command =  "cd " + self.getProjectPath() + " " + separator + " yo --no-color " + self.getComponent() + " " + name
		self.startCommand(command)

## Route
class RouteCommand(YoCommand):

	def getMessage(self):
		return "Router name:"

	def getComponent(self):
		return "angular:route"

## Controller
class ControllerCommand(YoCommand):

	def getMessage(self):
		return "Controller name:"

	def getComponent(self):
		return "angular:controller"

## Directive
class DirectiveCommand(YoCommand):

	def getMessage(self):
		return "Directive name:"

	def getComponent(self):
		return "angular:directive"

## Filter
class FilterCommand(YoCommand):

	def getMessage(self):
		return "Filter name:"

	def getComponent(self):
		return "angular:filter"

## View
class ViewCommand(YoCommand):

	def getMessage(self):
		return "View name:"

	def getComponent(self):
		return "angular:view"

## Factory
class FactoryCommand(YoCommand):

	def getMessage(self):
		return "Factory name:"

	def getComponent(self):
		return "angular:factory"

## Service
class ServiceCommand(YoCommand):

	def getMessage(self):
		return "Service name:"

	def getComponent(self):
		return "angular:service"

## Decorator
class DecoratorCommand(YoCommand):

	def getMessage(self):
		return "Decorator name:"

	def getComponent(self):
		return "angular:decorator"

## Provider
class ProviderCommand(YoCommand):

	def getMessage(self):
		return "Provider name:"

	def getComponent(self):
		return "angular:provider"

## Constant
class ConstantCommand(YoCommand):

	def getMessage(self):
		return "Constant name:"

	def getComponent(self):
		return "angular:constant"

## Value
class ValueCommand(YoCommand):

	def getMessage(self):
		return "Value name:"

	def getComponent(self):
		return "angular:value"
