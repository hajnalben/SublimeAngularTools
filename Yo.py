from . import Base

## ===========================================
## ================ Yeomann ==================
## ===========================================

class YoCommand(Base.InputCommand):

	def getModuleBaseCommand(self):
		return "yo --no-color"

	def process(self, name):
		command =  self.getComponent() + " " + name
		
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