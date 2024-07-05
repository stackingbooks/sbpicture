# creates and displays .SBP files (Stacking Books Picture)
# by stackingbooks

import PIL.Image
from textwrap import wrap
import zlib
import os
import sys
import contextlib

with contextlib.redirect_stdout(None):
    import pygame


def tosbp(pth):
    im = PIL.Image.open(os.path.join(os.path.abspath("."),pth)) # open the file user sent
    pix = im.load()
    data = ""
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            hex = '%02x%02x%02x%02x' % (pix[x,y][0],pix[x,y][1],pix[x,y][2],pix[x,y][3])
            data = data + hex
        data = data + '\n'
    
    compressed = zlib.compress(data.encode('utf8'))
    
    file_path = os.path.join(os.path.dirname(pth), os.path.splitext(os.path.basename(pth))[0] + ".sbp")
    file = open(file_path, 'wb')
    file.write(b'SBP' + compressed)
    file.close()
    return True
    
def viewsbp(pth):
    file = open(os.path.join(os.path.abspath("."),pth), "rb")  # read the file user sent
    file.seek(3)
    data = file.read()
    decompressed = zlib.decompress(data).decode('utf8')
    lines = decompressed[:-1].split('\n')
    
    xsize = 0
    ysize = 0
    
    
    # get the size of the epic picture!
    for i in range(len(lines)):
        line = wrap(lines[i], 8)
        xsize += 1
        ysize = len(line)
        
    
    # display it.
    
    pygame.display.init()
    
    icon = pygame.image.load('sbpviewer.png') 
    pygame.display.set_icon(icon)
    
    window = pygame.display.set_mode((max(xsize, 512), max(ysize, 512)))
    pygame.display.set_caption("Stacking Books Picture Viewer")
    
    surface = pygame.Surface((xsize, ysize))
    
    x = 0
    for i in range(len(lines)):
        line = wrap(lines[i], 8)
        x += 1
        y = 0
        for j in range(len(line)):
            y += 1
            color = line[j]
            rgba = tuple(int(color[k:k+2], 16) for k in (0, 2, 4, 6))
            alpha = rgba[3] / 255.0
            pcolor = pygame.Color(int(rgba[0] * alpha), int(rgba[1] * alpha), int(rgba[2] * alpha))
            surface.set_at((x,y), pcolor)
            
    x_offset = (max(xsize, 512) - xsize) // 2
    y_offset = (max(ysize, 512) - ysize) // 2
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        window.blit(surface, (x_offset, y_offset))
        pygame.display.flip()

    pygame.quit()

def fromsbp(pth, format):
    supported = ['png', 'tiff', 'webp']
    if format in supported:
        file_path = os.path.join(os.path.dirname(pth), os.path.basename(pth))
        file = open(file_path, 'rb')
        file.seek(3)
        compressed = file.read()
        file.close()
        
        data = zlib.decompress(compressed).decode('utf8')
        lines = data[:-1].split('\n')
        width = 0
        height = 0
    
    
        # get the size of the epic picture!
        for i in range(len(lines)):
            line = wrap(lines[i], 8)
            width += 1
            height = len(line)
        
        im = PIL.Image.new('RGBA', (width, height))
        pix = im.load()
        
        x = 0
        for i in range(len(lines)-1):
            line = wrap(lines[i+1], 8)
            x += 1
            y = 0
            for j in range(len(line)):
                hex = line[j]
                rgba = tuple(int(hex[k:k+2], 16) for k in (0, 2, 4, 6))
                pix[x, y] = rgba
                y += 1
        
        image_path = os.path.join(os.path.dirname(pth), os.path.splitext(os.path.basename(pth))[0] + "." + format)
        im.save(image_path)
        return True
    else:
        return False

if len(sys.argv) >= 4:
    mode = sys.argv[1]
    file = sys.argv[2]
    format = sys.argv[3]
    if mode == "-from":
        fromsbp(file,format)
elif len(sys.argv) >= 3:
    mode = sys.argv[1]
    file = sys.argv[2]
    if mode == "-to":
        tosbp(file)
    elif mode == "-view":
        viewsbp(file)
    else:
        viewsbp(file)
elif len(sys.argv) >= 2:
    file = sys.argv[1]
    viewsbp(file)
    
