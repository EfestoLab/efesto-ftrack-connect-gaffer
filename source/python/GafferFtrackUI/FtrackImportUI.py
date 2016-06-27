import logging

import IECore

import Gaffer
import GafferUI
import GafferFtrack

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


node = GafferFtrack.FtrackAbcImport

logger.info('registering node %s' % node)


Gaffer.Metadata.registerNode(
	node,
	"description",
	"""
	Ftrack Import Node
	""",
	plugs = {

		"fileName" : [

			"description",
			"""
			Description here...
			""",

			"plugValueWidget:type", "GafferUI.FileSystemPathPlugValueWidget",
			"pathPlugValueWidget:leaf", True,
			"pathPlugValueWidget:valid", True,
			"pathPlugValueWidget:bookmarks", "sceneCache",
			"fileSystemPathPlugValueWidget:extensions", IECore.StringVectorData( [ "abc" ] ),
		],

		"refreshCount" : [],

		"assetId" : [],
		"assetVersion" : [],
		"assetPath" : [],
		"assetTake" : [],
		"assetComponentId" : [],
	}
)

GafferUI.PlugValueWidget.registerCreator(
	node,
	"refreshCount",
	GafferUI.IncrementingPlugValueWidget,
	label = "Refresh",
	undoable = False
)

logger.info('node %s registered' % node)
