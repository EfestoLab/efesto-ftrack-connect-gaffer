import GafferUI

import GafferFtrack
import GafferFtrackUI

nodeMenu = GafferUI.NodeMenu.acquire( application )

nodeMenu.append(
    "/Ftrack/Import",
    GafferFtrack.FtrackImport,
    searchText="FtrackImport"
)
