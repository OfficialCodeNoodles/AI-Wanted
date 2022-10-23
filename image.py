import pyautogui
from PIL import Image

from properties import *

characterTextures = []
characterIcons = [] 
characterSubIcons = []

def loadCharacterTextures():
    for character in Character:
        texture = Image.open(f"assets/{character.name}.png")
        characterTextures.append(texture)

        icon = Image.open(f"assets/{character.name}Icon.png")
        characterIcons.append(icon)

properties = Properties() 

def generateIconSubregions(iconIndex) -> Image:
    iconSize = characterIcons[iconIndex].size

    # Num of columns to split icon into. 
    xSubRegions = 7
    # Num of rows to split icon into. 
    ySubRegions = 7
    subRegionWidth = iconSize[0] / xSubRegions
    subRegionHeight = iconSize[1] / ySubRegions

    for xRegion in range(0, xSubRegions):
        for yRegion in range(ySubRegions):
            # Area of new sub-icon. 
            bounds = (
                xRegion * subRegionWidth, yRegion * subRegionHeight, (xRegion 
                * subRegionWidth) + subRegionWidth, (yRegion * subRegionHeight)
                + subRegionWidth
            )
            yield characterIcons[iconIndex].crop(bounds)
def generateCharacterSubIcons():
    for character in Character:
        subIcons = []
        for subIcon in generateIconSubregions(character.value):
            pixelCount = 0
            emptyPixels = 0

            # Allows for reading color data from each pixel. 
            subIcon = subIcon.convert("RGBA")

            for pixel in Image.Image.getdata(subIcon):
                # Pixel is empty if it's alpha component is zero. 
                if pixel[3] == 0:
                    emptyPixels += 1
                pixelCount += 1
            
            # Adds sub-icon to array if doesn't contain transparent pixels. 
            if emptyPixels == 0:
                subIcons.append(subIcon)
        characterSubIcons.append(subIcons)
def removeDuplicateSubIcons():
    for character1 in Character:
        for character2 in Character:
            # Ensures same characters icons arent compared. 
            if character1.value == character2.value:
                continue
        
            for i, subIcon in enumerate(characterSubIcons[character2.value]):
                iconBounds = locate(subIcon, characterIcons[character1.value])

                # Removes sub-icon if it can be found in a different character.
                if iconBounds is not None:
                    characterSubIcons[character2.value].pop(i)

def getScreenshot(mainScreen=True) -> Image:
    # Takes a screenshot based on which screen is required. 
    screenshot = pyautogui.screenshot(
        region=properties.mainScreen if mainScreen else properties.subScreen)
    size = screenshot.size
    scale = properties.mainScreenScale if mainScreen else\
        properties.subScreenScale
    # Scales image to match original DS screen size. 
    screenshot = screenshot.resize( ( int(size[0] / scale), 
        int(size[1] / scale) ), Image.NEAREST)
    return screenshot
def locate(subImage, baseImage, confidence=0.98) -> (int):
    return pyautogui.locate(subImage, baseImage, confidence=confidence) 