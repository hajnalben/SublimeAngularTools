import sublime, sublime_plugin
import subprocess, os, signal
import urllib.request
from threading import Thread

## ===========================================
## ================ Base =====================
## ===========================================

class BaseCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.process()

	# Utility functions

	def startAsync(self, callback, args):
		thread = Thread(target = callback, args = args)
		thread.start()

	def startCommand(self, command):
		path = self.getProjectPath()
		separator = self.getSeparator()
		baseCommand = self.getModuleBaseCommand()

		command = "cd \"" + path + "\" " + separator + " " + baseCommand + " " + command

		self.startAsync(self.sub_process_cmd, [command])

	_process = None

	def sub_process_cmd(self, command):
		print("Running command: " + command)

		if (os.name != 'nt'):
			command = 'export PATH=/usr/local/bin/:$PATH ;' + command

		self._process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#self._process.wait()

		sublime.status_message("Command finished!")

		print("== Message:")

		for line in self._process.stdout:
			print(line.strip().decode('utf-8'))

		print("== Error:")

		for line in self._process.stderr:
			print(line.strip().decode('utf-8'))

	def getSeparator(self):
		return '&' if os.name == 'nt' else ';'

	def getProjectPath(self):
		return self.window.extract_variables()['project_path']

	def getCachePath(self):
		return sublime.cache_path()

	def file_get_contents(self, filename):
		with open(filename, encoding="utf8") as f:
			return f.read()

	def projectFileExists(self, filename):
		return os.path.exists(self.getProjectPath() + "/" + filename) 

	def projectFolderExists(self, folderName):
		return os.path.isdir(self.getProjectPath() + "/" + folderName) 

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
