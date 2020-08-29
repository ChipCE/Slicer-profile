# Copyright (c) 2019 fieldOfView
# The MaterialSettingsPlugin is released under the terms of the AGPLv3 or higher.

from UM.Settings.ContainerStack import ContainerStack
from UM.Application import Application

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot


class CustomStackProxy(QObject):

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)

        self._container_ids = []

        self._stack = ContainerStack("CustomStack" + str(id(self)))
        self._stack_id = self._stack.id
        self._stack.setDirty(False) # never save this stack

        Application.getInstance().getContainerRegistry().addContainer(self._stack)

    @pyqtProperty(str, constant = True)
    def stackId(self):
        return self._stack_id

    ##  Set the containerIds property.
    def setContainerIds(self, container_ids):
        if container_ids == self._container_ids:
            return
        self._container_ids = container_ids

        while(self._stack.getContainers()):
            self._stack.removeContainer(0)

        for container_id in container_ids:
            containers = Application.getInstance().getContainerRegistry().findContainers(id = container_id)
            if containers:
                self._stack.addContainer(containers[0])

        self._stack.setDirty(False) # never save this stack

        self.containerIdsChanged.emit()

    ##  Emitted when the containerIds property changes.
    containerIdsChanged = pyqtSignal()

    ##  The ID of the container we should query for property values.
    @pyqtProperty("QVariantList", fset = setContainerIds, notify = containerIdsChanged)
    def containerIds(self):
        return self._container_ids

    @pyqtSlot(str)
    def removeInstanceFromTop(self, key):
        self._stack.getTop().removeInstance(key)
        self._stack.getTop().setDirty(True)