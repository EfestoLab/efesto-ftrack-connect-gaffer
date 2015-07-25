import logging

import Gaffer
import GafferFtrack


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
        ],
        "another": [
            "description",
            """
            A String Plug widget
            """,
            "plugValueWidget:type",  # layout:widgetType : gaffer 0.14
            "GafferUI.StringPlugValueWidget",

        ]
    }
)

logger.info('node registered')
