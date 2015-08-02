import logging
import GafferUI
import GafferFtrack
import GafferFtrackUI

nodeMenu = GafferUI.NodeMenu.acquire( application )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('registering nodeMenu')

nodeMenu.append(
    "/Ftrack/AbcImport",
    GafferFtrack.FtrackAbcImport,
    searchText="FtrackAbcImport"
)
