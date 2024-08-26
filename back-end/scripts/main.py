import requests
import settings
import random
import time
from bs4 import BeautifulSoup

# Vars

errors = []
lastPage = 1

# Run

def runApplication():

    currentPageNum = 1
    global lastPage

    titles = []

    while currentPageNum <= lastPage:

        sleep_time = random.uniform(1, 4) 
        time.sleep(sleep_time)

        link = getLink(currentPageNum)

        print("\n CURRENT LINK: " + str(link) + "\n")

        htmlText = getHTMLText(link)

        if (isErrors == True):
            return
        
        bs = BeautifulSoup(htmlText, 'html.parser')

        card = settings.getHtmlSetting("card")
        pageButton = settings.getHtmlSetting("page_button")

        titleClass = card["title"]["class"]
        pageButtonClass = pageButton["class"]

        allTitles = bs.findAll('span', str(titleClass))
        allAvailablePagesLinks = bs.findAll('a', str(pageButtonClass))

        print(str(allAvailablePagesLinks))

        for currentTitle in allTitles:
            titles.append(str(currentTitle.text))

        for currentPage in allAvailablePagesLinks:
            pageNumber = getPageNumberFromLink(currentPage["href"])
            print("CURRENT PAGE HREF: " + str(currentPage["href"]))
            print("PAGE NUMBER: " + pageNumber)
            pageNumber = int(pageNumber)

            if (pageNumber > lastPage):
                lastPage = pageNumber

        print("\n LAST PAGE: " + str(lastPage) + "\n")

        currentPageNum += 1

    # for title in titles:
    #     print(title)

    
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

def getPageNumberFromLink(link):
    startIndex  = link.find("p=")

    if type(startIndex) != type(1):
        return 0
    else:
        startIndex = startIndex + 2
        endIndex    = link.find("&", startIndex)

        if type(endIndex) != type(1):
            endIndex = len(link - 1)

        return link[startIndex:endIndex]


def getLink(p = 1):
    urlSeparator = '/'
    paramSeparator = '&'

    url = settings.getRequestSetting("url")

    params = []

    dealType  = settings.getRequestSetting("deal_type")
    engineVersion = settings.getRequestSetting("engine_version")
    offerType = settings.getRequestSetting("offer_type")
    region = settings.getRequestSetting("region")
    rooms = settings.getRequestSetting("rooms")

    params.append("deal_type="       + str(dealType))
    params.append("engine_version="  + str(engineVersion))
    params.append("offer_type="      + str(offerType))
    params.append("p="               + str(p))
    params.append("region="          + str(region))
    # ++Rooms
    params.append("room1="           + str(rooms["room1"]))
    params.append("room2="           + str(rooms["room2"]))
    params.append("room3="           + str(rooms["room3"]))
    params.append("room4="           + str(rooms["room4"]))
    params.append("room5="           + str(rooms["room5"]))
    params.append("room6="           + str(rooms["room6"]))
    params.append("room7="           + str(rooms["room7"]))
    params.append("room9="           + str(rooms["room9"]))
    # --Rooms


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

