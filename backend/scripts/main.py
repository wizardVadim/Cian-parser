from logging import ERROR
from venv import logger

import requests
import settings
import random
import time
import datetime
import logging
import os
from bs4 import BeautifulSoup

from backend.scripts.settings import getLoggerSetting

# Vars

errors = []
lastPage = 1

# Run

def runApplication():

    logging.info("App has been STARTED: " + str(datetime.datetime.now().time()) + "\n OS: " + os.name + " " + os.getlogin())

    currentPageNum = 1
    global lastPage

    titles = []

    while currentPageNum <= lastPage:

        sleep_time = random.uniform(1, 4) 
        time.sleep(sleep_time)

        link = getLink(currentPageNum)

        logging.info("\n CURRENT LINK: " + str(link) + "\n")

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

        for currentTitle in allTitles:
            titles.append(str(currentTitle.text))

        # Update last page
        for currentPage in allAvailablePagesLinks:
            pageNumber = getPageNumberFromLink(currentPage["href"])
            logging.info("CURRENT PAGE HREF: " + str(currentPage["href"]))
            logging.info("PAGE NUMBER: " + str(pageNumber))
            pageNumber = int(pageNumber)

            if (pageNumber > lastPage):
                lastPage = pageNumber

        logging.info("\n LAST PAGE: " + str(lastPage) + "\n")

        currentPageNum += 1

    logging.info("Founded titles: \n" + titles)

    logging.info("\nApp has been ENDED: " + str(datetime.datetime.now().time()) + "\n OS: " + os.name + " " + os.getlogin())

    
# HTML Parsing

def getHTMLText(link):

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

    if type(startIndex) != type(1) or startIndex == -1:
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

def isErrors():

    global errors

    if len(errors) > 0:

        for i in errors:
            logging.error(i)

        return True
    
    return False

# Logging
def initLogger():

    loggingLevels = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    levelLog = loggingLevels[settings.getLoggerSetting("level")]

    loggerRoot = settings.getLoggerRoot()
    filenameLog = loggerRoot + "/" + getLoggerSetting("filename")

    logging.basicConfig(level=levelLog, filename=filenameLog, filemode="w")

# Init
try:
    initLogger()
    runApplication()
except Exception as exc:
    logging.critical(str(exc) + "\n" + str(exc.__context__))


