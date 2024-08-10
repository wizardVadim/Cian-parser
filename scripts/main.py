import requests
import settings

# Run

def runApplication():

    link = getLink()

    result = requests.get(link)

    if (result.status_code != 200):
        errorText = "Ошибка подключения к сайту"
        printError(errorText)
        return

    htmlText = result.text  
    print(result.status_code == 200)

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

# Init
runApplication()

