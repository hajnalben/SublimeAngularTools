from . import Base

## ===========================================
## ================ Grunt ====================
## ===========================================
## Needed functionalities:
##  - running custom task from bower.js
##  - killing serve node process
## ===========================================

class GruntCommand(Base.BaseCommand):

	def getModuleBaseCommand(self):
		return "grunt --no-color"

	def process(self):
		self.startCommand("")

class GruntServeCommand(GruntCommand):
	
	def process(self):

		if self._process is None:
			self.startCommand("serve")
		else:
			print(self._process.pid)
			##self._process.send_signal(signal.CTRL_C_EVENT)
			##os.kill(self._process.pid, signal.CTRL_C_EVENT)
			self._process.terminate()
			self._process = None

class GruntTestCommand(GruntCommand):

	def process(self):
		self.startCommand("test")

class GruntBuildCommand(GruntCommand):

	def process(self):
		self.startCommand("build")