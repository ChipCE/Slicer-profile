# Copyright (c) 2019 fieldOfView
# The MaterialSettingsPlugin is released under the terms of the AGPLv3 or higher.

from UM.Settings.Models.SettingDefinitionsModel import SettingDefinitionsModel

class MaterialSettingDefinitionsModel(SettingDefinitionsModel):

    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent = parent, *args, **kwargs)

    def _isDefinitionVisible(self, definition, **kwargs):
        # filter out any setting that is irrelevant for an extruder/material
        if getattr(definition, "settable_per_extruder") == False and getattr(definition, "resolve") is None:
            return False

        return super()._isDefinitionVisible(definition, **kwargs)
