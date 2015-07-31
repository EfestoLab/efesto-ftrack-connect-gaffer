# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import ftrack
from PySide import QtCore, QtGui

from ftrack_connect.ui.widget import entity_path as entityPath
from ftrack_connect.ui.widget import entity_browser as entityBrowser
from ftrack_connect.ui.theme import applyTheme


class AssetSelector(QtGui.QWidget):
    entityChanged = QtCore.Signal(object)

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

        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)

        # context_layout
        context_layout = QtGui.QHBoxLayout()
        context_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(context_layout)

        context_layout.addWidget(self.entityPath)
        context_layout.addWidget(self.entityBrowseButton)

        # asset_version_layout
        asset_version_layout = QtGui.QHBoxLayout()
        asset_version_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(asset_version_layout)

        self.assets_cb = QtGui.QComboBox()
        self.asset_v_cb = QtGui.QComboBox()

        asset_version_layout.addWidget(self.assets_cb)
        asset_version_layout.addWidget(self.asset_v_cb)

        # signals
        self.entityBrowseButton.clicked.connect(
            self._onEntityBrowseButtonClicked
        )
        self.entityChanged.connect(self.entityPath.setEntity)
        self.entityBrowser.selectionChanged.connect(
            self._onEntityBrowserSelectionChanged
        )
        self.entityBrowser.selectionChanged.connect(
            self.getAssets
        )
        self.setEntity(currentEntity)

        self.assets_cb.currentIndexChanged.connect(self.getVersions)

    def getVersions(self):
        selection = self.assets_cb.currentIndex()
        asset = self.assets_cb.itemData(selection)
        version = asset.getVersions()
        print version

    def getAssets(self):
        assets = self._entity.getAssets()
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
