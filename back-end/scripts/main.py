import requests
import settings
from bs4 import BeautifulSoup

# Vars

errors = []

# Run

def runApplication():

    link = getLink()

    htmlText = getHTMLText(link)

    if (isErrors == True):
        return
    
    bs = BeautifulSoup(htmlText, 'html.parser')

    card = settings.getHtmlSetting("card")

    cardClass = card["class"]

    titleClass = card["title"]["class"]

    allTitles = bs.findAll('span', str(titleClass))

    for i in allTitles:
        print(i.text)
    
# HTML Parsing

def getHTMLText(link): 

    link = getLink()

    result = requests.get(link)

    if (result.status_code != 200):
        errorText = "Ошибка подключения к сайту. Код ответа: " + str(result.status_code)
        global errors
        errors.append(errorText)
        return ""
    
    return result.text

# Link

def getLink(p = 1):
    urlSeparator = '/'
    paramSeparator = '&'

    url = settings.getRequestSetting("url")

    params = []

    dealType  = settings.getRequestSetting("deal_type")
    engineVersion = settings.getRequestSetting("engine_version")
    offerType = settings.getRequestSetting("offer_type")
    region = settings.getRequestSetting("region")

    params.append("deal_type="       + str(dealType))
    params.append("engine_version="  + str(engineVersion))
    params.append("offer_type="      + str(offerType))
    params.append("p="               + str(p))
    params.append("region="          + str(region))

    paramsStr = paramSeparator.join(params)

    paramsStr = "cat.php?" + paramsStr

    link = []

    link.append(url)
    link.append(paramsStr)

    linkStr = urlSeparator.join(link)
    return linkStr

# Error

def printError(errorText):

    print("Error: " + errorText)

def isErrors():

    global errors

    if len(errors) > 0:

        for i in errors:
            printError(i)

        return True
    
    return False

# Init

runApplication()

