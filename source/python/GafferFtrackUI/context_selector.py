# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import logging
from PySide import QtCore, QtGui

import ftrack

from ftrack_connect.ui.widget import entity_path as entityPath
from ftrack_connect.ui.widget import entity_browser as entityBrowser
from ftrack_connect.ui.theme import applyTheme

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetSelector(QtGui.QWidget):
    entityChanged = QtCore.Signal(object)
    importComponent = QtCore.Signal(object)

    def __init__(self, currentEntity, parent=None):
        '''Initialise ContextSelector widget with the *currentEntity* and
        *parent* widget.
        '''
        super(AssetSelector, self).__init__(parent=parent)
        self._entity = currentEntity
        self.entityBrowser = entityBrowser.EntityBrowser()
        self.entityBrowser.setMinimumWidth(600)
        self.entityPath = entityPath.EntityPath()
        self.entityBrowseButton = QtGui.QPushButton('Browse')
        applyTheme(self.entityBrowser)
        applyTheme(self.entityBrowser.overlay)

        self.selectedComponentPath = None

        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        self.import_button = QtGui.QPushButton('import selected component')
        # context_layout
        context_layout = QtGui.QHBoxLayout()
        context_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(context_layout)

        context_layout.addWidget(self.entityPath)
        context_layout.addWidget(self.entityBrowseButton)

        # asset_version_layout
        asset_version_layout = QtGui.QHBoxLayout()
        asset_version_layout.setContentsMargins(0, 0, 0, 0)

        self.assets_cb = QtGui.QComboBox()
        self.asset_v_cb = QtGui.QComboBox()

        asset_version_layout.addWidget(self.assets_cb)
        asset_version_layout.addWidget(self.asset_v_cb)
        main_layout.addLayout(asset_version_layout)

        # component
        components_layout = QtGui.QHBoxLayout()
        components_layout.setContentsMargins(0, 0, 0, 0)

        self.components_cb = QtGui.QComboBox()
        components_layout.addWidget(self.components_cb)
        main_layout.addLayout(components_layout)

        # import button
        main_layout.addWidget(self.import_button)

        # signals
        self.entityBrowseButton.clicked.connect(
            self._onEntityBrowseButtonClicked
        )
        self.entityChanged.connect(self.entityPath.setEntity)
        self.entityBrowser.selectionChanged.connect(
            self._onEntityBrowserSelectionChanged
        )
        self.entityBrowser.selectionChanged.connect(
            self.on_getAssets
        )

        self.assets_cb.currentIndexChanged.connect(self.on_getVersions)
        self.asset_v_cb.currentIndexChanged.connect(self.on_getComponents)
        self.import_button.clicked.connect(self.on_importComponent)
        self.setEntity(currentEntity)

    def on_importComponent(self):
        selection = self.components_cb.currentIndex()
        component = self.components_cb.itemData(selection)
        file_path = component.getFilesystemPath()
        logger.info('emitting: %s' % file_path)
        self.selectedComponentPath = file_path
        self.importComponent.emit(file_path)

    def on_getComponents(self):
        selection = self.asset_v_cb.currentIndex()
        version = self.asset_v_cb.itemData(selection)
        if not version:
            return
        components = version.getComponents()
        self.components_cb.clear()
        for component in components:
            if component.getFileType() != '.abc':
                continue
            self.components_cb.addItem(str(component.getName()), component)

    def on_getVersions(self):
        selection = self.assets_cb.currentIndex()
        asset = self.assets_cb.itemData(selection)
        if not asset:
            return
        versions = asset.getVersions()
        self.asset_v_cb.clear()
        for version in versions:
            self.asset_v_cb.addItem(str(version.getVersion()), version)

    def on_getAssets(self):
        assets = self._entity.getAssets()
        if not assets:
            return
        self.assets_cb.clear()
        for asset in assets:
            name = asset.getName()
            self.assets_cb.addItem(name, asset)

    def reset(self, entity=None):
        '''reset browser to the given *entity* or the default one'''
        currentEntity = entity or self._entity
        self.entityPath.setEntity(currentEntity)
        self.setEntity(currentEntity)

    def setEntity(self, entity):
        '''Set the *entity* for the view.'''
        self._entity = entity
        self.entityChanged.emit(entity)

    def _onEntityBrowseButtonClicked(self):
        '''Handle entity browse button clicked.'''
        # Ensure browser points to parent of currently selected entity.
        if self._entity is not None:
            location = []
            try:
                parents = self._entity.getParents()
            except AttributeError:
                pass
            else:
                for parent in parents:
                    location.append(parent.getId())

            location.reverse()
            self.entityBrowser.setLocation(location)

        # Launch browser.
        if self.entityBrowser.exec_():
            selected = self.entityBrowser.selected()
            if selected:
                self.setEntity(selected[0])
            else:
                self.setEntity(None)

    def _onEntityBrowserSelectionChanged(self, selection):
        '''Handle selection of entity in browser.'''
        self.entityBrowser.acceptButton.setDisabled(True)
        if len(selection) == 1:
            entity = selection[0]

            # Prevent selecting Projects or Tasks directly under a Project to
            # match web interface behaviour.
            if isinstance(entity, ftrack.Task):
                objectType = entity.getObjectType()
                if (
                    objectType == 'Task'
                    and isinstance(entity.getParent(), ftrack.Project)
                ):
                    return

                self.entityBrowser.acceptButton.setDisabled(False)
