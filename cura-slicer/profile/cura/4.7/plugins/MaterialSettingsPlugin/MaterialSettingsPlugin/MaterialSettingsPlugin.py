# Copyright (c) 2019 fieldOfView
# The MaterialSettingsPlugin is released under the terms of the AGPLv3 or higher.

import os.path

from cura.CuraApplication import CuraApplication
from UM.Extension import Extension
from UM.Resources import Resources
from UM.Logger import Logger

from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtCore import QUrl

from . import MaterialSettingsPluginVisibilityHandler

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

class MaterialSettingsPlugin(Extension):
    def __init__(self):
        super().__init__()

        self._settings_dialog = None

        self.setMenuName(catalog.i18nc("@item:inmenu", "Material Settings"))
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Configure Material Settings"), self.showSettingsDialog)

        default_material_settings = {
            "default_material_print_temperature",
            "default_material_bed_temperature",
            "material_standby_temperature",
            #"material_flow_temp_graph",
            "cool_fan_speed",
            "retraction_amount",
            "retraction_speed",
            "material_flow",
        }

        CuraApplication.getInstance().getPreferences().addPreference(
            "material_settings/visible_settings",
            ";".join(default_material_settings)
        )

        CuraApplication.getInstance().engineCreatedSignal.connect(self._onEngineCreated)

    def _onEngineCreated(self):
        qmlRegisterType(
            MaterialSettingsPluginVisibilityHandler.MaterialSettingsPluginVisibilityHandler,
            "Cura", 1, 0, "MaterialSettingsVisibilityHandler"
        )

        # Adding/removing pages from the preferences dialog is handles in QML
        # There is no way to access the preferences dialog directly, so we have to search for it
        preferencesDialog = None
        for child in CuraApplication.getInstance().getMainWindow().contentItem().children():
            try:
                test = child.setPage # only PreferencesDialog has a setPage function
                preferencesDialog = child
                break
            except:
                pass

        if preferencesDialog:
            Logger.log("d", "Replacing Materials preferencepane with patched version")
            materialPreferences = QUrl.fromLocalFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "qml", "MaterialPreferences", "MaterialsPage.qml"))

            preferencesDialog.removePage(3)
            preferencesDialog.insertPage(3, catalog.i18nc("@title:tab", "Materials"), materialPreferences.toString())
        else:
            Logger.log("e", "Could not replace Materials preferencepane with patched version")

    def showSettingsDialog(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qml", "SettingsDialog.qml")
        self._settings_dialog = CuraApplication.getInstance().createQmlComponent(path, {"manager": self})
        self._settings_dialog.show()
