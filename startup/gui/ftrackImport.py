import GafferUI
import GafferFtrack

nodeMenu = GafferUI.NodeMenu.acquire( application )

nodeMenu.append(
    "/Ftrack/Import",
    GafferFtrack.FtrackImport,
    searchText="FtrackImport"
)
