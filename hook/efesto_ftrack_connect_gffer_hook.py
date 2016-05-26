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

GAFFER_ROOT = os.environ.get(
    'GAFFER_ROOT',
    '/home/efesto/apps/gaffer-0.24.0.0-linux'
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
            gaffer_root = GAFFER_ROOT
            path = gaffer_root.split(os.sep)
            path[0] = os.sep
            path.append('bin')
            path.append('^gaffer$')
            print path

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


    def _setupGafferEnvs(self, environment):

        root = GAFFER_ROOT
        environment = ftrack_connect.application.appendPath(
            root, 'GAFFER_ROOT', environment
        )

        glsl = os.path.join(GAFFER_ROOT, 'glsl')
        environment = ftrack_connect.application.appendPath(glsl, 'IECOREGL_SHADER_PATHS', environment)
        environment = ftrack_connect.application.appendPath(glsl, 'IECOREGL_SHADER_INCLUDE_PATHS', environment)

        fonts = os.path.join(GAFFER_ROOT, 'fonts')
        environment = ftrack_connect.application.appendPath(fonts, 'IECORE_FONT_PATHS', environment)

        op = os.path.join(GAFFER_ROOT, 'ops')
        local_op = os.path.join(os.getenv('HOME'), 'gaffer', 'ops')
        environment = ftrack_connect.application.appendPath(op, 'IECORE_OP_PATHS', environment)
        environment = ftrack_connect.application.appendPath(local_op, 'IECORE_OP_PATHS', environment)

        op_preset = os.path.join(GAFFER_ROOT, 'opPresets')
        local_op_preset = os.path.join(os.getenv('HOME'), 'gaffer', 'opPresets')
        environment = ftrack_connect.application.appendPath(op_preset, 'IECORE_OP_PRESET_PATHS', environment)
        environment = ftrack_connect.application.appendPath(local_op_preset, 'IECORE_OP_PRESET_PATHS', environment)

        proc_path =  os.path.join(GAFFER_ROOT, 'procedurals')
        local_proc_path = os.path.join(os.getenv('HOME'), 'gaffer', 'procedurals')
        environment = ftrack_connect.application.appendPath(proc_path, 'IECORE_PROCEDURAL_PATHS', environment)
        environment = ftrack_connect.application.appendPath(local_proc_path, 'IECORE_PROCEDURAL_PATHS', environment)
        
        proc_preset_path = os.path.join(GAFFER_ROOT, 'proceduralPresets')
        local_proc_preset_path = os.path.join(os.getenv('HOME'), 'gaffer', 'proceduralPresets')
        environment = ftrack_connect.application.appendPath(proc_preset_path, 'IECORE_PROCEDURAL_PRESET_PATHS', environment)
        environment = ftrack_connect.application.appendPath(local_proc_preset_path, 'IECORE_PROCEDURAL_PRESET_PATHS', environment)

        tiles =  os.path.join(GAFFER_ROOT, 'resources','cortex','tileset_2048.dat')
        environment = ftrack_connect.application.appendPath(tiles, 'CORTEX_POINTDISTRIBUTION_TILESET', environment)

        apps =  os.path.join(GAFFER_ROOT, 'apps')
        local_apps = os.path.join(os.getenv('HOME'), 'gaffer', 'apps')
        environment = ftrack_connect.application.appendPath(apps, 'GAFFER_APP_PATHS', environment)
        environment = ftrack_connect.application.appendPath(local_apps, 'GAFFER_APP_PATHS', environment)

        startup = os.path.join(GAFFER_ROOT, 'startup')
        local_startup = os.path.join(os.getenv('HOME'), 'gaffer', 'startup')
        environment = ftrack_connect.application.appendPath(startup, 'GAFFER_STARTUP_PATHS', environment)
        environment = ftrack_connect.application.appendPath(local_startup, 'GAFFER_STARTUP_PATHS', environment)

        gui_image_path = os.path.join(GAFFER_ROOT, 'graphics') 
        environment = ftrack_connect.application.appendPath(gui_image_path, 'GAFFERUI_IMAGE_PATHS', environment)

        oslhome = GAFFER_ROOT
        environment = ftrack_connect.application.appendPath(oslhome, 'OSLHOME', environment)

        library_path = os.path.join(GAFFER_ROOT, 'lib') 
        environment = ftrack_connect.application.appendPath(library_path, 'LD_LIBRARY_PATH', environment)

        path = os.path.join(GAFFER_ROOT, 'bin')
        environment = ftrack_connect.application.appendPath(path, 'PATH', environment)

        appleseed = os.path.join(GAFFER_ROOT, 'appleseed')
        environment = ftrack_connect.application.appendPath(appleseed, 'APPLESEED', environment)

        appleseed_lib = os.path.join(appleseed, 'lib')
        environment = ftrack_connect.application.appendPath(appleseed_lib, 'LD_LIBRARY_PATH', environment)

        appleseed_python = os.path.join(appleseed, 'lib', 'python2.7')
        environment = ftrack_connect.application.appendPath(appleseed_python, 'PYTHONPATH', environment)

        appleseed_search_path = os.path.join(appleseed, 'shaders')
        gaffer_display = os.path.join(GAFFER_ROOT, 'appleseedDisplays')
        environment = ftrack_connect.application.appendPath(appleseed_search_path, 'APPLESEED_SEARCHPATH', environment)
        environment = ftrack_connect.application.appendPath(gaffer_display, 'APPLESEED_SEARCHPATH', environment)

        appleseed_bin = os.path.join(appleseed, 'bin')
        environment = ftrack_connect.application.appendPath(path, 'PATH', environment)

        return environment

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

        # environment = self._setupGafferEnvs(environment)

        gaffer_connect_path = os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, 'python')
        environment = ftrack_connect.application.appendPath(
            gaffer_connect_path, 'PYTHONPATH', environment
        )

        gaffer_startup_path = os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, 'startup')
        environment = ftrack_connect.application.appendPath(
            gaffer_startup_path, 'GAFFER_STARTUP_PATHS', environment
        )

        # OVERRIDES
        # QTPLUGINS svg & xml

        resource_folder =  os.path.abspath(os.path.join(EFESTO_FTRACK_CONNECT_GAFFER_PATH, '..', 'resource'))

        qt_plugins_path = os.path.abspath(os.path.join(resource_folder, 'qt_plugins'))
        environment = ftrack_connect.application.appendPath(
            qt_plugins_path, 'QT_PLUGIN_PATH', environment
        )


        pyside_libraries = os.path.abspath(os.path.join(resource_folder, 'pyside'))
        environment = ftrack_connect.application.appendPath(
            pyside_libraries, 'LD_LIBRARY_PATH', environment
        )

        environment = ftrack_connect.application.appendPath(
            pyside_libraries, 'PYTHONPATH', environment
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
