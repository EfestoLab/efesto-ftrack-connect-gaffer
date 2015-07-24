import Gaffer
import GafferUI
import GafferScene
import GafferFtrack

Gaffer.Metadata.registerNode(
    GafferFtrack.FtrackImport,

    "description",
    """
    Ftrack Import Node
    """,

    plugs={
        "asset": [
            "description",
            """
            Provide a custom widget
            """,

            "plugValueWidget:type",
            "GafferFtrackUI.MyWidgetPlugValue",
        ]
    }
)
