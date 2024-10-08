import json
from pathlib import Path

def parseSettingsJSON(rootPath):
    return json.load(open(str(rootPath / 'settings.json')))

def getSettings():
    return settings

def getRequestSetting(settingsName):
    return settings["request"][settingsName]

def getHtmlSetting(settingsName):
    return settings["html"][settingsName]

def getLoggerSetting(settingName):
    return settings["logger"][settingName]

def getLoggerRoot():
    return (str(Path(__file__).resolve().parents[1] / 'logs'))

rootPath = Path(__file__).resolve().parents[1]
settings = parseSettingsJSON(rootPath)
    
