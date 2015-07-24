import Gaffer
import GafferUI
import GafferScene
import GafferFtrack
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('registering node...')


Gaffer.Metadata.registerNode(
    GafferFtrack.FtrackImport,

    "description",
    """
    Ftrack Import Node
    """,

    plugs={
        "fileName": [
            "description",
            """
            Provide a custom widget
            """,

            "plugValueWidget:type",  # layout:widgetType : gaffer 0.14
            "GafferFtrackUI.MyWidgetPlugValue",
        ]
    }
)

logger.info('node registered')
