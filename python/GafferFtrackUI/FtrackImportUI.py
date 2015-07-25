import logging

import Gaffer
import GafferFtrack

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


node = GafferFtrack.FtrackImport

logger.info('registering node %s' % node)


Gaffer.Metadata.registerNode(
    node,
    "description",
    """
    Ftrack Import Node
    """,

    plugs={
        "fileName": [

            "description",

            """
            Provide a custom widget.
            """,

            "nodule:type", "",
            # "layout:section", "User",
            "plugValueWidget:type",  # layout:widgetType : gaffer 0.14
            "GafferFtrackUI.MyWidgetPlugValue",
        ],

        "another": [

            "description",

            """
            A String Plug widget.
            """,

            "nodule:type", "",
            "plugValueWidget:type",
            "GafferUI.StringPlugValueWidget",

        ]
    }
)

logger.info('node %s registered' % node)
