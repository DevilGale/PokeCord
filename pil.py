from PIL import Image
from io import BytesIO
import requests

import random
import time
import numpy as np
import sys

white = (255,255,255) #255
black = (0, 0, 0) #255
transparent = (255, 255, 255) #0

def getPokemon(val):
    url = "http://pokeapi.co/api/v2/pokemon/" + val + "/"
    t0 = time.clock()
    poke = requests.get(url).json()
    print("Obtained Pokemon - " + str(time.clock() - t0))
    return poke

def getGIFimage(name):
    response = requests.get("https://play.pokemonshowdown.com/sprites/xyani/" + name.lower() + ".gif")
    print("Obtained Image: {}".format(response))
    frames = Image.open(BytesIO(response.content))
    return frames

def simpleCollage(frames):
    i = 0
    width, height = frames.size
    compilation =  Image.new('RGBA', size=(width * 5, height * 5))
    p = frames.getpalette()
    doOnce = True

    try:                
        while True:
            if i <= 25:
                compilation.paste(frames, box=(width * divmod(i,6)[1], height * divmod(i,6)[0]))
            if not frames.getpalette():
                frames.putpalette(p)
                print("Put Palette")
            if doOnce:

                # print(frames.getpalette())
                print(frames.getcolors())
                doOnce = False
            frames.seek(frames.tell() + 1)
            i = i + 1
    except EOFError:
        pass
    compilation.show()  

def GIFconvertBW(frames):
    frames.seek(0)
    p = frames.getpalette()
    last_frame = frames.convert('RGBA')
    all_frames = []
    try:
        while True:
            hitBlackLine = False
            colorsToCheck = [transparent]
            if not frames.getpalette():
                frames.putpalette(p)

            current_frame = frames.convert('RGB')   
            pixdata = current_frame.load()
            width, height = current_frame.size
            for x in range(0, width - 1):
                for y in range(0, height - 1):
                    if hitBlackLine:
                        if pixdata[x,y] not in colorsToCheck:
                            pixdata[x,y] = black
                        else:
                            pixdata[x,y] = white
                    else:
                        if pixdata[x,y] <= (60,60,60):
                            hitBlackLine = True
                        elif pixdata[x,y] not in colorsToCheck:
                            colorsToCheck.append(pixdata[x,y])
                            # pixdata[x,y] = white
                # hitBlackLine = False

                    #Option 1#################################        
                    # if hitBlackLine:
                    #     if pixdata[x,y] not in colorsToCheck:
                    #         pixdata[x,y] = black
                    #     else:
                    #         pixdata[x,y] = white
                    # else:
                    #     if pixdata[x,y] <= (60,60,60):
                    #         hitBlackLine = True
                    #     elif pixdata[x,y] not in colorsToCheck:
                    #         colorsToCheck.append(pixdata[x,y])
                    ###########################################
                    # if not hitBlackLine and pixdata[x,y] != black:
                    #     colorsToCheck.append(pixdata[x,y])
                    #     print(pixdata[x,y])

                    # elif not hitBlackLine and pixdata[x,y] == black:
                    #     hitBlackLine = True
                    # elif pixdata[x,y] not in colorsToCheck:
                    #     pixdata[x,y] = black
            current_frame = current_frame.convert('RGBA')
            all_frames.append(current_frame)
            frames.seek(frames.tell() + 1)
            print("Frame {}: {}".format(frames.tell(), colorsToCheck[:4]))
    except EOFError:
        pass
    all_frames[0].save("test.gif", save_all=True, optimize=True, append_images=all_frames[1:], loop=1000)
    simpleCollage(Image.open("test.gif"))

def main():
    print("Entered: {}".format(sys.argv))
    # If random pokemon wanted
    if len(sys.argv) == 1:
        poke = getPokemon(str(random.randint(1,200)))
        frames = getGIFimage(poke['name'])
    # If specific number wanted
    elif sys.argv[1].isdigit():
        poke = getPokemon(sys.argv[1])
        frames = getGIFimage(poke['name'])
    # If pokemon name is known
    else:
        frames = getGIFimage(sys.argv[1])
    simpleCollage(frames)
    GIFconvertBW(frames)
    exit()



def getStillImg(pokeObj):
    response = requests.get(poke['sprites']['front_default'])
    print("Obtained Image")
    img = Image.open(BytesIO(response.content))
    img.save('original.png')
    shape_img = img.convert('RGBA')
    pixdata = shape_img.load()
    width, height = shape_img.size
    hit_pixel = False
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            #Check if color is transparent
            if pixdata[x,y] == (0, 0, 0, 0):
                if hit_pixel == True:
                    pixdata[x - 1,y] = white
                    hit_pixel = False
                else:
                    continue
            #If not then is part of image
            else:
                if hit_pixel == True:
                    pixdata[x,y] = black
                else:
                    pixdata[x,y] = white
                    hit_pixel = True

            # if pixdata[x,y] != (0, 0, 0, 0) and hit_pixel == False:
            #     pixdata[x,y] = (255, 255, 255, 255)
            #     hit_pixel = True
            # elif pixdata[x,y] != (0, 0, 0, 0) and hit_pixel == True:
            #     pixdata[x,y] = (0, 0, 0, 255)
            # elif pixdata[x,y] == (0, 0, 0, 0) and hit_pixel == True:
            #     pixdata[x-1, y] = (255,255,255,255)
            #     hit_pixel = False


    shape_img.save('test_image.png')


main()