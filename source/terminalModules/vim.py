import terminalModuleHandler
import tones
import textInfos
import api
import core
import speech

MODE_INVALID = -1
MODE_INSERT = 0
MODE_NORMAL = 1
class TerminalModule(terminalModuleHandler.TerminalModule):
	lastMode = MODE_INVALID
	_shouldDie = True

	def reportMode(self):
		tones.beep((500 if self.mode==MODE_INSERT else 800), 100)

	def _get_mode(self):
		focus = api.getFocusObject()
		ti=focus.makeTextInfo(textInfos.POSITION_LAST)
		ti.expand(textInfos.UNIT_LINE)
		if ti.text.find("-- INSERT --")+1:
			return MODE_INSERT
		else:
			return MODE_NORMAL

	def _moniter(self):
		if self.mode!=self.lastMode:
			self.lastMode = self.mode
			self.reportMode()
		if not self._shouldDie:
			core.callLater(100, self._moniter)

	def event_terminalModule_activate(self, obj):
		self._shouldDie = False
		self._moniter()

	def event_terminalModule_deactivate(self, obj):
		self._shouldDie = True

	def script_normalModeCharMove(self, gesture):
		if self.mode == MODE_INSERT:
			gesture.send()
			return
		obj = api.getFocusObject()
		obj._caretMovementScriptHelper(gesture, textInfos.UNIT_CHARACTER)

	def script_normalModeWordMove(self, gesture):
		if self.mode == MODE_INSERT:
			gesture.send()
			return
		obj = api.getFocusObject()
		obj._caretMovementScriptHelper(gesture, textInfos.UNIT_WORD)

	def script_normalModeWordEndMove(self, gesture):
		if self.mode == MODE_INSERT:
			gesture.send()
			return
		obj = api.getFocusObject()
		obj._caretMovementScriptHelper(gesture, textInfos.UNIT_WORD)
		ti = obj.makeTextInfo(textInfos.POSITION_CARET)
		ti.expand(textInfos.UNIT_CHARACTER)
		speech.speakText(ti.text)

	def script_normalModeLineMove(self, gesture):
		if self.mode == MODE_INSERT:
			gesture.send()
			return
		obj = api.getFocusObject()
		obj._caretMovementScriptHelper(gesture, textInfos.UNIT_LINE)


	__gestures = {
		"kb:h" : "normalModeCharMove",
		"kb:l" : "normalModeCharMove",
		"kb:w" : "normalModeWordMove",
		"kb:e" : "normalModeWordEndMove",
		"kb:b" : "normalModeWordMove",
		"kb:j" : "normalModeLineMove",
		"kb:k" : "normalModeLineMove",
	}