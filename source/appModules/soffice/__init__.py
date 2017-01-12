#appModules/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2017 NV Access, Derek Riemer

import appModuleHandler
import controlTypes
from compoundDocuments import CompoundDocument
from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
from NVDAObjects.JAB import JAB, JABTextInfo

import documentObjects
import calc

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		role=obj.role
		windowClassName=obj.windowClassName
		if isinstance(obj, IAccessible) and windowClassName in ("SALTMPSUBFRAME", "SALSUBFRAME", "SALFRAME"):
			if role==controlTypes.ROLE_TABLECELL:
				clsList.insert(0, documentObjects.SymphonyTableCell)
			elif hasattr(obj, "IAccessibleTextObject"):
				clsList.insert(0, documentObjects.SymphonyText)
			if role==controlTypes.ROLE_PARAGRAPH:
				clsList.insert(0, documentObjects.SymphonyParagraph)
		if isinstance(obj, JAB) and windowClassName == "SALFRAME":
			if role in (controlTypes.ROLE_PANEL,controlTypes.ROLE_LABEL):
				parent=obj.parent
				if parent and parent.role==controlTypes.ROLE_TABLE:
					clsList.insert(0, calc.JAB_OOTableCell)
			elif role==controlTypes.ROLE_TABLE:
				clsList.insert(0, calc.JAB_OOTable)

	def event_NVDAObject_init(self, obj):
		windowClass = obj.windowClassName
		if isinstance(obj, JAB) and windowClass == "SALFRAME":
			# OpenOffice.org has some strange role mappings due to its use of JAB.
			if obj.role == controlTypes.ROLE_CANVAS:
				obj.role = controlTypes.ROLE_DOCUMENT

		if windowClass in ("SALTMPSUBFRAME", "SALFRAME") and obj.role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_TEXTFRAME) and obj.description:
			# This is a word processor document.
			obj.description = None
			obj.treeInterceptorClass = CompoundDocument
