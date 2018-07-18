#IAccProcServer.py:
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Implementation of IAccProcServer, so that customization of a wx control can be done very fast."""

from logHandler import log
from  comtypes.automation import VT_EMPTY
from  comtypes import COMObject
from comInterfaces.Accessibility import IAccPropServer

class IAccPropServer_Impl(COMObject):
	"""Base class for implementing a COM interface for AccPropServer.
	Please override the _GetPropValue method, not GetPropValue.
	GetPropValue wraps _getPropValue to catch and log exceptions (Which for some reason NVDA's logger misses when they occur in GetPropValue).
	"""
	
	_com_interfaces_ = [
		IAccPropServer
	]

	def __init__(self, control, *args, **kwargs):
		"""Initialize the instance of AccPropServer. 
		@param control: the WX control instance, so you can look up things in the _getPropValue method.
			It's available on self.control.
		@Type control: Subclass of wx.Window
		"""
		self.control = control
		super(IAccPropServer_Impl, self).__init__(*args, **kwargs)

	def _getPropValue(self, pIDString, dwIDStringLen, idProp):
		"""use this method to implement GetPropValue. It  is wrapped by the callback GetPropValue to handle exceptions.
		See https://msdn.microsoft.com/en-us/library/windows/desktop/dd373681(v=vs.85).aspx for instructions on implementing accPropServers.
		See https://msdn.microsoft.com/en-us/library/windows/desktop/dd318495(v=vs.85).aspx for instructions specifically about this method.
		@param pIDString: Contains a string that identifies the property being requested.
		@type pIDString: A weird comtypes thing you should not mess with.
		@param dwIDStringLen: Specifies the length of the identity string specified by the pIDString parameter.
		@type dwIDStringLen: technically dwordd
		@param idProp: Specifies a GUID indicating the desired property.
		@type idProp: One of the oleacc.PROPID_* GUIDS
		"""
		raise NotImplementedError

	def GetPropValue(self, pIDString, dwIDStringLen, idProp):
		try:
			return self._getPropValue(pIDString, dwIDStringLen, idProp)
		except Exception:
			log.exception()
			return VT_EMPTY, 0

