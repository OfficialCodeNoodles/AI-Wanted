import time

from image import *

refreshRate = 2
characterMatch = None
prvsCharacterMatch = None
characterMatchTicks = 0 

def loadApplication():
    loadCharacterTextures()
    generateCharacterSubIcons()
    removeDuplicateSubIcons()
    properties.loadFile()
    # This failsafe isn't neccesary as I have built one in already. 
    pyautogui.FAILSAFE = False
def updateSearch():
    global characterMatch, prvsCharacterMatch, characterMatchTicks

    mainScreen = getScreenshot()
    subScreen = getScreenshot(mainScreen=False)

    foundCharacter = None

    # Searches to find the character that is wanted. 
    for character in Character:
        characterBounds = locate(characterTextures[character.value], 
            mainScreen, confidence=0.75)
        
        if characterBounds is not None:
            foundCharacter = character
            characterMatchTicks += 60 / refreshRate
            break
    
    if foundCharacter is None or prvsCharacterMatch != characterMatch:
        characterMatchTicks = 0
        characterMatch = None
    else:
        # Starts icon search after one second. 
        if characterMatchTicks >= 60:
            characterMatch = foundCharacter

    prvsCharacterMatch = characterMatch

    if characterMatch is not None:
        # A box that represents the on screen area of the icon searched for. 
        iconBounds = locate(characterIcons[characterMatch.value], subScreen, 
            confidence=0.9)

        # If the icon is found, press the icon. 
        if iconBounds is not None:
            pressIcon(iconBounds)
        # Otherwise search using small sections of the icon. 
        else:
            for i, subIcon in enumerate(characterSubIcons[characterMatch.value]):
                iconBounds = locate(subIcon, subScreen)

                if iconBounds is not None:
                    pressIcon(iconBounds)
                    return
def pressIcon(bounds):
    # Finds center of the icon. 
    iconCenter = pyautogui.center(bounds)
    position = ( 
        ( iconCenter[0] * properties.subScreenScale ) 
            + properties.subScreen[0],                 
        ( iconCenter[1] * properties.subScreenScale ) 
            + properties.subScreen[1]
    )

    # Clicks on the icon. 
    pyautogui.moveTo(position[0], position[1])
    pyautogui.drag(0.0, 1.0, 0.15)

if __name__ == "__main__":
    try:
        loadApplication()
    except Exception as exception:
        print(exception)
        exit()

    # Confirmation box to start the program. 
    if pyautogui.confirm(
        "Welecome to the Wanted AI! The image recongnition will only work if" 
        + " the variables in the properties file are correct, so make sure to"
        + " update them if needed.",
        title="Wanted AI", buttons=["Begin", "Cancel"]
    ) == "Cancel":
        exit()

    applicationClosed = False

    while not applicationClosed:
        updateSearch()

        time.sleep(1.0 / refreshRate)

        # Emergency exits the program when the mouse is in the top left corner. 
        mousex, mousey = pyautogui.position()
        applicationClosed = mousex + mousey == 0