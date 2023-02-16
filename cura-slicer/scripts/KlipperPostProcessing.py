'''Mesh area is based on script by frankbags@https://gist.github.com/frankbags/c85d37d9faff7bce67b6d18ec4e716ff '''
import re  # To perform the search and replace.
from ..Script import Script


class KlipperPostProcessing(Script):

    def getSettingDataString(self):
        return """{
            "name": "Klipper Post Processing",
            "key": "KlipperPostProcessing",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "enable_dynamic_scv":
                {
                    "label": "Dynamic Square Corner Velocity(SCV)",
                    "description": "Enable dynamic Square Corner Velocity",
                    "type": "bool",
                    "default_value": true
                },
                "default_scv":
                {
                    "label": "    Default SCV",
                    "description": "Default Square Corner Velocity",
                    "type": "int",
                    "default_value": 5,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "outer_wall_scv":
                {
                    "label": "    Outer wall SCV",
                    "description": "Outer wall Square Corner Velocity",
                    "type": "int",
                    "default_value": 5,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "inner_wall_scv":
                {
                    "label": "    Inner wall SCV",
                    "description": "Inner wall Square Corner Velocity",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "skin_scv":
                {
                    "label": "    Skin SCV",
                    "description": "Skin Square Corner Velocity",
                    "type": "int",
                    "default_value": 15,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "infill_scv":
                {
                    "label": "    Infill SCV",
                    "description": "Infill Square Corner Velocity",
                    "type": "int",
                    "default_value": 20,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "enable_dynamic_mesh_area":
                {
                    "label": "Dynamic bed mesh area",
                    "description": "Dynamically changing the bed mesh area based on the size of the parts will be printed. Custom BED_MESH_CALIBRATE macro, AREA_START and AREA_END parameters are required in the start G-code.",
                    "type": "bool",
                    "default_value": true
                },
                "enable_layer_progress_report":
                {
                    "label": "Layer progress report",
                    "description": "Enable layer progress report.",
                    "type": "bool",
                    "default_value": true
                }
            }
        }"""

    def execute(self, data):
        enable_dynamic_scv = self.getSettingValueByKey("enable_dynamic_scv")
        default_scv = self.getSettingValueByKey("default_scv")
        outer_wall_scv = self.getSettingValueByKey("outer_wall_scv")
        inner_wall_scv = self.getSettingValueByKey("inner_wall_scv")
        skin_scv = self.getSettingValueByKey("skin_scv")
        infill_scv = self.getSettingValueByKey("infill_scv")
        enable_dynamic_mesh_area = self.getSettingValueByKey("enable_dynamic_mesh_area")
        enable_layer_progress_report = self.getSettingValueByKey("enable_layer_progress_report")

        minMaxXY = {'MINX': 0, 'MINY': 0, 'MAXX': 0, 'MAXY': 0}
        startGcodeLineData = ''
        totalLayerCount = ''
        currentLayer = ''

        for layerNumber, layerData in enumerate(data):
            
            if enable_layer_progress_report:
                # get total layer count
                if not totalLayerCount:
                    result = re.search(r";LAYER_COUNT:(\d*)", data[layerNumber])
                    if result is not None:
                        totalLayerCount = result.group(1)
                # get current layer count
                if totalLayerCount:
                    result = re.search(r";LAYER:(\d*)", data[layerNumber])
                    if result is not None:
                        currentLayer = result.group(1)

                # insert progress code before the layer data
                if currentLayer and totalLayerCount:
                    data[layerNumber] = "LAYER_PROGRESS TOTAL_LAYER=" + str(totalLayerCount) + " CURRENT_LAYER=" + str(currentLayer)+ "\n" + data[layerNumber]

            if enable_dynamic_mesh_area:
                # search for print area boundary
                for k, v in minMaxXY.items():
                    result = re.search(str(k)+":(\d*\.?\d*)", data[layerNumber])
                    if result is not None:
                        minMaxXY[k] = result.group(1)
                # search for set print area macro
                areaStartGcode = re.search(
                    ".*%(MINX|MAXX|MINY|MAXY)%.*", data[layerNumber])
                # replace print area template
                if areaStartGcode is not None:
                    if not startGcodeLineData:
                        startGcodeLineData = data[layerNumber]
                    for k, v in minMaxXY.items():
                        pattern3 = re.compile('%' + k + '%')
                        startGcodeLineData = re.sub(
                            pattern3, v, startGcodeLineData)
                    data[layerNumber] = startGcodeLineData
            
            if enable_dynamic_scv:
                lines = data[layerNumber].split("\n")
                for lineNumber,lineData in enumerate(lines):
                    if lineData.startswith(";TYPE:FILL"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(infill_scv)
                    elif lineData.startswith(";TYPE:WALL-INNER"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(inner_wall_scv)
                    elif lineData.startswith(";TYPE:WALL-OUTER"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(outer_wall_scv)
                    elif lineData.startswith(";TYPE:SKIN"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(skin_scv)
                    elif lineData.startswith(";TYPE:") or lineData.startswith(";LAYER:"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(default_scv)
                    else:
                        continue
                    
                data[layerNumber] = "\n".join(lines)

        return data
