# Copyright (c) 2019 fieldOfView
# The MaterialSettingsPlugin is released under the terms of the AGPLv3 or higher.

from . import MaterialSettingsPlugin
from . import MaterialSettingDefinitionsModel
from . import CustomStackProxy

from PyQt5.QtQml import qmlRegisterType


def getMetaData():
    return {}

def register(app):
    qmlRegisterType(CustomStackProxy.CustomStackProxy, "MaterialSettingsPlugin", 1, 0, "CustomStack")
    qmlRegisterType(MaterialSettingDefinitionsModel.MaterialSettingDefinitionsModel, "MaterialSettingsPlugin", 1, 0, "MaterialSettingDefinitionsModel")

    return {"extension": MaterialSettingsPlugin.MaterialSettingsPlugin()}
