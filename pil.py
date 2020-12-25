from PIL import Image, ImageDraw, ImageFont, ImageColor
from io import BytesIO
import requests

import random
import time
import math
import sys

white = (255,255,255) #255
black = (0, 0, 0) #255
transparent = (255, 255, 255) #0

def getPokemon(val):
    url = "http://pokeapi.co/api/v2/pokemon/" + val + "/"
    t0 = time.time()
    poke = requests.get(url).json()
    print(f"Obtained Pokemon - {time.time() - t0}")
    return poke

def getGIFimage(name):
    response = requests.get(f"https://play.pokemonshowdown.com/sprites/xyani/{name.lower()}.gif")
    print(f"Obtained Image: {response} : {response.url}")
    frames = Image.open(BytesIO(response.content))
    return frames

def simpleCollage(frames, num_images_width : int = 5, num_images_height : int = 10, fit : bool = False):
    width, height = frames.size
    if fit:
        num_images_height = math.ceil(frames.n_frames / num_images_width)
    print(f"Frames in image ({num_images_width}x{num_images_height}): {frames.n_frames} - {frames.filename if frames.filename else 'N/A'}")
    compilation = Image.new('RGBA', size=(width * num_images_width, height * num_images_height))
    fnt = ImageFont.load_default().font
    last_dispose_method_2 = 0
    for i in range(frames.n_frames):
        frames.seek(i)
        the_frame = frames.convert()
        draw = ImageDraw.Draw(the_frame)
        draw.rectangle(frames.dispose_extent, outline=(0,0,0,255))
        draw.text((0,0), f"F{i}-M{frames.disposal_method}", font=fnt, fill=(255, 0, 0))

        compilation.alpha_composite(
            the_frame, 
            dest=(
                width * int(i % num_images_width), 
                height * int(i / num_images_width)
                )
            )
        if frames.disposal_method == 2:
            last_dispose_method_2 = i
        frames.seek(0)
        if i == (num_images_width * num_images_height):
            break;
    compilation.show()
    compilation.save("compilation.png")  

def reformCollage(frames, num_images_width : int = 5, num_images_height : int = 10, fit : bool = False):
    # frames.seek(27)
    # frames.show()
    width, height = frames.size
    if fit:
        num_images_height = math.ceil(frames.n_frames / num_images_width)
    print(f"Frames in image ({num_images_width}x{num_images_height}): {frames.n_frames} - {frames.filename}")
    frames.seek(0)
    backgroundColor = frames.info['background']
    compilation = Image.new('RGBA', size=(width * num_images_width, height * num_images_height), color=(255, 255, 0))#, color=(255,0,0))
    fnt = ImageFont.load_default().font
    #print(f"Disposal Method - {frames.disposal_method}, Disposal Extend - {frames.dispose_extent}, Info - {frames.info}")
    for i in range(frames.n_frames):
        frames.seek(i)
        the_frame = Image.new('RGBA', size=frames.size)
        pixdata = the_frame.load()

        for x in range(width):
            for y in range(height):
                palette = frames.getpalette()
                a_pixel = frames.getpixel((x,y))
                if a_pixel == frames.info['transparency']:
                    pixdata[x, y] = (0, 255, 255, 0)
                    #pixdata[x,y] = tuple(palette[a_pixel:a_pixel+3] + [100])
                elif a_pixel == frames.info['background']:
                    pixdata[x, y] = (255, 0 , 0, 255)
                else:
                    pixdata[x,y] = tuple(palette[a_pixel:a_pixel+3])# + [255])
        #the_frame.alpha_composite(frames, dest=frames.dispose_extent[0:2], source=frames.dispose_extent)
        #the_frame = frames.convert()

        draw = ImageDraw.Draw(the_frame)
        draw.rectangle(frames.dispose_extent, outline=(255,173,0,255))
        # draw.text((0,0), f"F{i}-M{frames.disposal_method}", font=fnt, fill=(255, 0, 0))

        compilation.alpha_composite(
            the_frame, 
            dest=(
                width * int(i % num_images_width), 
                height * int(i / num_images_width)
                )
            )
        if i == (num_images_width * num_images_height):
            break;
    compilation.show()
    compilation.save("compilation.png")  

def GIFconvertBW(frames):
    width, height = frames.size
    all_frames = []

    corrected_prev_frame = None
    pass_frame = Image.new('RGBA', size=frames.size, color=(255,255,255,0))
    #disposal_method_list = []
    for i in range(frames.n_frames):
        frames.seek(i)
        if i == 4:
            frames.save(f"frames_{i}.png")
        disp_frame, pass_frame = method_dispose(i, frames, pass_frame)
        frames.seek(0)
        disp_frame = disp_frame.convert('RGB')

        pixdata = disp_frame.load()
        #Change Colors
        for x in range(width):
            for y in range(height):
                if pixdata[x,y] != white:
                    pixdata[x,y] = black

        disp_frame = disp_frame.convert('P')
        all_frames.append(disp_frame)


    print(f"Save {len(all_frames)} frames in 'test.gif'")
    all_frames[0].save(
        fp="test.gif", 
        format='GIF',
        save_all=True, 
        append_images=all_frames[1:], 
        optimize=False,
        duration=frames.info['duration'],
        loop=0,
        disposal=1,
        transparency=255,
        background=0
        )
    simpleCollage(Image.open("test.gif"), 12, fit=True)

##########################################
#         Frame Process Methods          #
##########################################

#crop_frame = current_frame.crop(frames.dispose_extent)
#new_frame.alpha_composite(crop_frame, dest=frames.dispose_extent[0:2])

def method_dispose(i, frames, previous_frame):
    # 0 PIL = Overlay and pass
    # 1 PIL = Overlay and return previous
    # 2 PIL = Erase Overlay
    new_frame = previous_frame.copy()
    current_frame = frames.convert()

    new_frame.alpha_composite(current_frame, dest=frames.dispose_extent[0:2], source=frames.dispose_extent)
    if frames.disposal_method == 0:
        return new_frame, Image.new('RGBA', box=frames.size)
    elif frames.disposal_method == 1:
        return new_frame, new_frame.copy()
    elif frames.disposal_method == 2 or frames.disposal_method == 3:
        draw = ImageDraw.Draw(previous_frame)
        draw.rectangle(frames.dispose_extent, fill=(white + (0,)))
        return new_frame, previous_frame.copy()
    else:
        print("UNKNOWN disposal_method")
        exit()

def method_sum_check(i, current_frame : Image, previous_frame :  Image, size_opt_color):
    width, height = current_frame.size
    if previous_frame is None:
            disp_frame = current_frame.copy()
    else:
        #Remove borders
        pixdata = current_frame.load()
        if size_opt_color is not None:
            if pixdata[0, 0] == size_opt_color:
                for x in range(width):
                    for y in range(height):
                        if pixdata[x, y] == size_opt_color:
                            pixdata[x,y] = white + (0, )
                        # elif pixdata[x, y][3] == 255:
                        #     break;

                    # for y in range(height - 1, -1, -1):
                    #     if pixdata[x, y] == size_opt_color:
                    #         pixdata[x, y] = white + (0, )
                    #     elif pixdata[x, y][3] == 255:
                    #         break;
        curr_alpha_sum = 0
        prev_alpha_sum = 0
        prev_pixdata = previous_frame.load()
        for x in range(width):
            for y in range(height):
                if prev_pixdata[x, y][3] == 0:
                    prev_alpha_sum += 1
                if pixdata[x, y][3] == 0:
                    curr_alpha_sum += 1


        percent_diff = (curr_alpha_sum / prev_alpha_sum) * 100.0
        if percent_diff > 109.0: # or percent_diff > 100.0: #percent
            #print(f"{i} = {percent_diff:6.2f}%: Check Sum (Prev-{prev_alpha_sum} vs Curr-{curr_alpha_sum})")
            disp_frame = Image.alpha_composite(previous_frame, current_frame)
        else:
            #print(f"\t{i} = {percent_diff:6.2f}%: Check Sum (Prev-{prev_alpha_sum} vs Curr-{curr_alpha_sum})")
            disp_frame = current_frame.copy()
   
    pre_recolor = disp_frame.copy()

    return disp_frame, pre_recolor

def method_simple_recolor(current_frame : Image):
    width, height = current_frame.size
    pixdata = current_frame.load()
    for x in range(width):
        for y in range(height):
            if pixdata[x,y][3] is 255:
                pixdata[x,y] = black + (255,)
            else:
                pixdata[x,y] = white + (255,)
    return current_frame

def method_gather_colors(current_frame : Image, hitBlackLine = False, colorsToCheck = [transparent]):
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

##########################################


def main():
    print("Args Entered: {}".format(sys.argv))
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
    print(frames.info)
    simpleCollage(frames, 12, fit=True)
    GIFconvertBW(frames)

    #import pdb; pdb.set_trace()




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