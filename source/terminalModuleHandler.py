#terminalModuleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Derek Riemer

import api
import pkgutil
import config
import baseObject
from logHandler import log
import ui
import terminalModules

#: List of all modules.
modules = []
#: The currently active module.
currentModule = 0

def getCurrentModule():
	return modules[currentModule]

def listTerminalModules():
	for loader, name, isPkg in pkgutil.iter_modules(terminalModules.__path__):
		if name.startswith("_"):
			continue
		try:
			tm = __import__("terminalModules.%s" % name, globals(), locals(), ("terminalModules",)).TerminalModule
		except:
			log.error("Error importing Terminal Module %s" % name, exc_info=True)
			continue
		yield tm

def setNextModule():
	global currentModule
	if currentModule is None or len(modules) == 1:
		return
	focus = api.getFocusObject()
	modules[currentModule].event_terminalModule_deactivate(focus)
	currentModule = (currentModule+1) % len(modules)
	modules[currentModule].event_terminalModule_activate(focus)
	ui.message(modules[currentModule].name)

def initialize():
	global modules
	config.addConfigDirsToPythonPackagePath(terminalModules)
	#Append the default module, so the user can select the behavior of having no module active.
	modules.append(DefaultTerminalModule())
	for module in listTerminalModules():
		try:
			modules.append(module())
		except:
			log.error("Error initializing Terminal Module %r" % plugin, exc_info=True)

def terminate():
	for module in modules:
		try:
			module.terminate()
		except:
			log.exception("Error terminating Terminal Module %r" % plugin)

class TerminalModule(baseObject.ScriptableObject):
	"""Base Terminal Module.
	TerminalModules facilitate the implementation of accessibility fixes for terminal apps, where traditional appModules are useless.
	Each Terminal Module should be a separate Python module in the terminalModules package containing a C{TerminalModule} class which inherits from this base class.
	TerminalModules can implement and bind gestures to scripts which will take effect at all times when the module is active, and when a terminal has focus.
	See L{ScriptableObject} for details.
	Terminal Modules can also receive NVDAObject events for all NVDAObjects that are terminals.
	This is done by implementing methods called C{event_eventName},
	where C{eventName} is the name of the event; e.g. C{event_gainFocus}.
	These event methods take two arguments: the NVDAObject on which the event was fired
	and a callable taking no arguments which calls the next event handler.
	Two events, event_terminalModule_activate and event_terminalModule_deactivate are defined, and called when this terminal module becomes active, and when it is deactivated. This occurs when the user presses nvda+space in terminals. This can be used to do things such as look for a line of text and say things.
	The C{name} of a module must be provided, so that the user can know what module is being activated.
	This can be done with a property, i.e. def _get_name if a dynamic name is needed.
	By default, the name of a Terminal Module  is the name of the deepest of its module, space seperated on underscores, (_). This aims to provide a reasonable name for most modules, however name should be overrided in many cases.
	"""

	def _get_name(self):
		name = self.__module__
		name = name.split(".")[-1]
		return name.replace("_", " ")

	def event_terminalModule_activate(self, obj):
		"""This event is fired when a terminalModule is activated by the user."""

	def event_terminalModule_deactivate(self, obj):
		"""This event is fired when a terminalModule is deactivated by the user in responce to another terminal module being activated."""

	def terminate(self):
		"""Terminate this Terminal Module.
		This will be called when NVDA is finished with this Terminal Module.
		"""

class DefaultTerminalModule(TerminalModule):
	"""Default terminal module, representing the No terminal Modules mode."""
	name = "No Terminal Module active"