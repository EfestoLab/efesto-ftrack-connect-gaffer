# :coding: utf-8
# :copyright: Copyright (c) 2015 Efesto Lab LTD

import getpass
import sys
import pprint
import logging
import re
import os

import ftrack
import ftrack_connect.application


EFESTO_FTRACK_CONNECT_GAFFER_PATH = os.environ.get(
    'EFESTO_FTRACK_CONNECT_GAFFER_PATH', 
     os.path.abspath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'source')
    )
)

GAFFER_INSTALL_PATH=os.environ.get(
    'GAFFER_INSTALL_PATH',
    '/home/efesto/Desktop/gaffer-0.24.0.0-linux'
)


class LaunchApplicationAction(object):
    '''Discover and launch gaffer.'''

    identifier = 'efesto-ftrack-connect-launch-gaffer'

    def __init__(self, application_store, launcher):
        '''Initialise action with *applicationStore* and *launcher*.

        *applicationStore* should be an instance of
        :class:`ftrack_connect.application.ApplicationStore`.

        *launcher* should be an instance of
        :class:`ftrack_connect.application.ApplicationLauncher`.

        '''
        super(LaunchApplicationAction, self).__init__()

        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )

        self.application_store = application_store
        self.launcher = launcher

    def is_valid_selection(self, selection):
        '''Return true if the selection is valid.'''
        if (
            len(selection) != 1 or
            selection[0]['entityType'] != 'task'
        ):
            return False

        entity = selection[0]
        task = ftrack.Task(entity['entityId'])

        if task.getObjectType() != 'Task':
            return False

        return True

    def register(self):
        '''Register discover actions on logged in user.'''
        ftrack.EVENT_HUB.subscribe(
            'topic=ftrack.action.discover and source.user.username={0}'.format(
                getpass.getuser()
            ),
            self.discover
        )

        ftrack.EVENT_HUB.subscribe(
            'topic=ftrack.action.launch and source.user.username={0} '
            'and data.actionIdentifier={1}'.format(
                getpass.getuser(), self.identifier
            ),
            self.launch
        )

    def discover(self, event):
        '''Return discovered applications.'''

        if not self.is_valid_selection(
            event['data'].get('selection', [])
        ):
            return

        items = []
        applications = self.application_store.applications
        applications = sorted(
            applications, key=lambda application: application['label']
        )

        for application in applications:
            application_identifier = application['identifier']
            label = application['label']
            items.append({
                'actionIdentifier': self.identifier,
                'label': label,
                'icon': application.get('icon', 'default'),
                'applicationIdentifier': application_identifier
            })

        return {
            'items': items
        }

    def launch(self, event):
        '''Handle *event*.

        event['data'] should contain:

            *applicationIdentifier* to identify which application to start.

        '''
        # Prevent further processing by other listeners.
        event.stop()

        if not self.is_valid_selection(
            event['data'].get('selection', [])
        ):
            return

        application_identifier = (
            event['data']['applicationIdentifier']
        )

        context = event['data'].copy()
        context['source'] = event['source']

        application_identifier = event['data']['applicationIdentifier']
        context = event['data'].copy()
        context['source'] = event['source']

        return self.launcher.launch(
            application_identifier, context
        )


class ApplicationStore(ftrack_connect.application.ApplicationStore):

    def _discoverApplications(self):
        '''Return a list of applications that can be launched from this host.

        An application should be of the form:

            dict(
                'identifier': 'name_version',
                'label': 'Name version',
                'path': 'Absolute path to the file',
                'version': 'Version of the application',
                'icon': 'URL or name of predefined icon'
            )

        '''
        applications = []

        if sys.platform == 'linux2':
            gaffer_install_path = GAFFER_INSTALL_PATH
            path = gaffer_install_path.split(os.sep)
            path[0] = os.sep
            path.append('bin')
            path.append('gaffer')

            applications.extend(self._searchFilesystem(
                expression=path,
                label='Gaffer',
                variant='{version}',
                applicationIdentifier='gaffer_{version}',
                icon='gaffer'
            ))

        self.logger.debug(
            'Discovered applications:\n{0}'.format(
                pprint.pformat(applications)
            )
        )
        return applications


class ApplicationLauncher(ftrack_connect.application.ApplicationLauncher):
    '''Custom launcher to modify environment before launch.'''

    def __init__(self, application_store, plugin_path):
        '''.'''
        super(ApplicationLauncher, self).__init__(application_store)

        self.plugin_path = plugin_path

    def _getApplicationEnvironment(
        self, application, context=None
    ):
        '''Override to modify environment before launch.'''

        # Make sure to call super to retrieve original environment
        # which contains the selection and ftrack API.
        environment = super(
            ApplicationLauncher, self
        )._getApplicationEnvironment(application, context)

        entity = context['selection'][0]
        task = ftrack.Task(entity['entityId'])
        taskParent = task.getParent()

        try:
            environment['FS'] = str(int(taskParent.getFrameStart()))
        except Exception:
            environment['FS'] = '1'

        try:
            environment['FE'] = str(int(taskParent.getFrameEnd()))
        except Exception:
            environment['FE'] = '1'

        environment['FTRACK_TASKID'] = task.getId()
        environment['FTRACK_SHOTID'] = task.get('parent_id')

        gaffer_connect_path = os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, 'python')
        environment = ftrack_connect.application.appendPath(
            gaffer_connect_path, 'PYTHONPATH', environment
        )

        gaffer_startup_path = os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, 'startup')
        environment = ftrack_connect.application.appendPath(
            gaffer_startup_path, 'GAFFER_STARTUP_PATHS', environment
        )

        qt_plugins_path = os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, '..', 'resource', 'qt_plugins')
        environment = ftrack_connect.application.appendPath(
            qt_plugins_path, 'QT_PLUGIN_PATH', environment
        )

        pyside_libraries = os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, '..', 'resource', 'pyside')
        environment = ftrack_connect.application.appendPath(
            pyside_libraries, 'LD_LIBRARY_PATG', environment
        )       

        print environment
        return environment


def register(registry, **kw):
    '''Register hooks.'''

    logger = logging.getLogger(
        'ftrack_plugin:efesto-ftrack_connect_gaffer_hook.register'
    )
    # Validate that registry is an instance of ftrack.Registry. If not,
    # assume that register is being called from a new or incompatible API and
    # return without doing anything.
    if not isinstance(registry, ftrack.Registry):
        logger.debug(
            'Not subscribing plugin as passed argument {0!r} is not an '
            'ftrack.Registry instance.'.format(registry)
        )
        return

    # Create store containing applications.
    application_store = ApplicationStore()

    # Create a launcher with the store containing applications.
    launcher = ApplicationLauncher(application_store, None)

    # Create action and register to respond to discover and launch actions.
    action = LaunchApplicationAction(application_store, launcher)
    action.register()
