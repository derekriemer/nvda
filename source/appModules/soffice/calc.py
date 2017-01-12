#appModules/calc.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

import controlTypes
import textInfos
from NVDAObjects.JAB import JAB, JABTextInfo

def gridCoordStringToNumbers(coordString):
	if not coordString or len(coordString)<2 or ' ' in coordString or coordString[0].isdigit() or not coordString[-1].isdigit(): 
		raise ValueError("bad coord string: %r"%coordString) 
	rowNum=0
	colNum=0
	coordStringRowStartIndex=None
	for index,ch in enumerate(reversed(coordString)):
		if not ch.isdigit():
			coordStringRowStartIndex=len(coordString)-index
			break
	rowNum=int(coordString[coordStringRowStartIndex:])
	for index,ch in enumerate(reversed(coordString[0:coordStringRowStartIndex])):
		colNum+=((ord(ch.upper())-ord('A')+1)*(26**index))
	return rowNum,colNum


class JAB_OOTable(JAB):

	def _get_rowCount(self):
		return 0

	def _get_columnCount(self):
		return 0

class JAB_OOTableCell(JAB):

	role=controlTypes.ROLE_TABLECELL

	def _get_name(self):
		name=super(JAB_OOTableCell,self).name
		if name and name.startswith('Cell') and name[-2].isdigit():
			return None
		return name

	def _get_cellCoordsText(self):
		name=super(JAB_OOTableCell,self).name
		if name and name.startswith('Cell') and name[-2].isdigit():
			return name[5:-1]

	def _get_value(self):
		value=super(JAB_OOTableCell,self).value
		if not value and issubclass(self.TextInfo,JABTextInfo):
			value=self.makeTextInfo(textInfos.POSITION_ALL).text
		return value

	def _get_states(self):
		states=super(JAB_OOTableCell,self).states
		states.discard(controlTypes.STATE_EDITABLE)
		return states

	def _get_rowNumber(self):
		try:
			return gridCoordStringToNumbers(self.cellCoordsText)[0]
		except ValueError:
			return 0

	def _get_columnNumber(self):
		try:
			return gridCoordStringToNumbers(self.cellCoordsText)[1]
		except ValueError:
			return 0

