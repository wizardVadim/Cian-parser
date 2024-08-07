import json
from pathlib import Path

def parseSettingsJSON(rootPath):
    return json.load(open(str(rootPath / 'settings.json')))

def getSettings():
    return settings

settings = ""


rootPath = Path(__file__).resolve().parents[1]
settings = parseSettingsJSON(rootPath)
    
