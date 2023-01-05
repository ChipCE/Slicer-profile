''' Based on script by frankbags@https://gist.github.com/frankbags/c85d37d9faff7bce67b6d18ec4e716ff '''
import re  # To perform the search and replace.
from ..Script import Script


class SnakeOilXYLayerProgress(Script):

    def getSettingDataString(self):
        return """{
            "name": "SnakeOilXY leyer progress",
            "key": "SnakeOilXYLayerProgress",
            "metadata": {},
            "version": 2,
            "settings":{}
        }"""

    def execute(self, data):
        totalLayerCount = ''
        currentLayer = ''
        gcodeTotalPrintTime = ''
        gcodeRemainPrintTime = ''
        gcodePercentProgress = ''

        for layerNumber, layerData in enumerate(data):
            # get total layer count
            if not totalLayerCount:
                result = re.search(r";LAYER_COUNT:(\d*)", layerData)
                if result is not None:
                    totalLayerCount = result.group(1)
            # get current layer count
            if totalLayerCount:
                result = re.search(r";LAYER:(\d*)", layerData)
                if result is not None:
                    currentLayer = result.group(1)
            # get total print time
            if not gcodeTotalPrintTime:
                result = re.search(r";TIME:(\d*)", layerData)
                if result is not None:
                    gcodeTotalPrintTime = float(result.group(1))
            # get current print time and calc progress percent
            if gcodeTotalPrintTime:
                result = re.search(r";TIME_ELAPSED:(\d*\.?\d*)", layerData)
                if result is not None:
                    timeElapsed = float(result.group(1))
                    gcodePercentProgress = int(
                        timeElapsed / gcodeTotalPrintTime * 100)
                    gcodeRemainPrintTime = str(int((gcodeTotalPrintTime - timeElapsed)/3600)) + ":" + str(
                        int((gcodeTotalPrintTime - timeElapsed) // 60 % 60))

            # insert progress code
            if currentLayer and gcodeRemainPrintTime and gcodePercentProgress:
                data[layerNumber] = "GCODE_PROGRESS TOTAL_LAYER=" + str(totalLayerCount) + " CURRENT_LAYER=" + str(
                    currentLayer) + " PROGRESS=" + str(gcodePercentProgress) + " REMAIN=" + str(gcodeRemainPrintTime) + "\n" + layerData

        return data

# layer progress format
# GCODE_PROGRESS TOTAL_LAYER=37 CURRENT_LAYER=0 PROGRESS=4 REMAIN=0:5