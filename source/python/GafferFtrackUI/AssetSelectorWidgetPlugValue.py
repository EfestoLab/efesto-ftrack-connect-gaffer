from __future__ import with_statement
import logging
import os

import IECore
import Gaffer
import GafferUI
import GafferFtrack

import ftrack

from AssetSelector import AssetSelector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QtCore = GafferUI._qtImport("QtCore")
QtGui = GafferUI._qtImport("QtGui")


class AssetSelectorWrapper(GafferUI.Widget):
	'''Create a wrapper around my custom widget'''

	def __init__(self, *args, **kw):
		logger.info('creating: %s ' % self.__class__.__name__)
		entity = os.getenv(
			'FTRACK_TASKID',
			os.getenv('FTRACK_SHOTID', '1ca0f86e-1d6e-11e5-b7ab-04013398c801')
		)
		# hardcoded Id for testing if not running through the hook

		current_entity = ftrack.Task(entity)
		self.AssetSelector = AssetSelector(current_entity)

		super(AssetSelectorWrapper, self).__init__(
			self.AssetSelector,
			toolTip='AssetSelector',
			**kw
		)
		self.__importComponentSignal = GafferUI.WidgetSignal()
		self._qtWidget().importComponent.connect(
			Gaffer.WeakMethod(self.__importComponent)
		)

	def importComponentSignal(self):
		return self.__importComponentSignal

	def __importComponent(self, state):
		logger.info(state)
		self.__importComponentSignal(self)

	def getValue(self):
		return self.AssetSelector.selectedComponentPath


class AssetSelectorPlugValue(GafferUI.PlugValueWidget):
	'''Create a plug value using my custom widget'''

	def __init__(self, plug, **kw):
		logger.info('creating: %s ' % self.__class__.__name__)

		self.__AssetSelector = AssetSelectorWrapper()
		super(AssetSelectorPlugValue, self).__init__(self.__AssetSelector, plug, **kw)
		self.__importComponentConnection = self.__AssetSelector.importComponentSignal().connect(
			Gaffer.WeakMethod(self.__importComponent)
		)
		self._updateFromPlug()

	def _updateFromPlug(self):
		pass
		# if self.getPlug() is not None:
		#	 with self.getContext():
		#		 with Gaffer.BlockedConnection(self.__stateChangedConnection):
		#			 self.__AssetSelector.setState(self.getPlug().getValue())

	def __importComponent(self, value):
		logger.info(value)
		with Gaffer.UndoContext(self.getPlug().ancestor(Gaffer.ScriptNode)):
			self.getPlug().setValue(self.__AssetSelector.getValue())
