from terminalModuleHandler import TerminalModule
import tones

class TerminalModule(TerminalModule):
	def script_beep(self, gesture):
		tones.beep(500,500)

	def event_typedCharacter(self, obj,  nextHandler, ch=None):
		tones.beep(800,800)
		nextHandler()

	__gestures = {
		"kb:nvda+shift+i":"beep",
	}