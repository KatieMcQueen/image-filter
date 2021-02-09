from PIL import Image
import numpy as np
imageName = input("Enter the name of the image to open: ")
filterName = input("What filter should we apply?> ")
shiftFilters = ['hue']
if filterName in shiftFilters:
    shift = input('how much shift?> ')
    shift = int(shift)
    shiftMode = input("What shift mode should be used?> ")
im = Image.open(imageName)
a = np.asarray(im)


def getPixelMatrix(img):
    pixels = list(img.getdata())
    matrix = []
    for i in range(0, len(pixels), img.width):
        matrix.append(pixels[i:i+img.width])
    return matrix

def rgb2hsl(pixel):
    r = pixel[0]/256
    g = pixel[1]/256
    b = pixel[2]/256
    maxColor = max(r,g,b)
    minColor = min(r,g,b)
    if minColor == maxColor:
        h = 0.0
        s = 0.0
        l = r
    else:
        l = (minColor + maxColor) / 2
        if l < .5:
            s = (maxColor - minColor)/(maxColor + minColor)
        else:
            s = (maxColor - minColor)/(2.0 - maxColor - minColor)
        if maxColor == r:
            h = (g - b) / (maxColor - minColor)
        elif maxColor == g:
            h = 2.0 + (b - r) / (maxColor - minColor)
        else:
            h = 4.0 + (r-g) / (maxColor - minColor)
        h /= 6.0
        if h < 0:
            h += 1
    h *= 255
    s *= 255
    l *= 255
    return [h,s,l]

def hsl2rgb(pixel):
    h = pixel[0]/256
    s = pixel[1]/256
    l = pixel[2]/256
    if s == 0:
        r = g = b = l
    else:
        #setting up temporary variables
        if l < 0.5:
            temp2 = l*(l+s)
        else:
            temp2 = (l+s)-(l*s)
        temp1 = 2 * l - temp2
        tempr = (h+1.0)/3.0
        if tempr > 1:
            tempr -= 1
        tempg = h
        tempb = (h - 1.0)/3.0
        if tempb < 0:
            tempb += 1

        #red
        if tempr < 1.0 / 6.0:
            r = temp1 + (temp2 - temp1) * 6.0 * tempr
        elif tempr < 0.5:
            r = temp2
        elif tempr < 2.0 / 3.0:
            r = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempr) * 6.0
        else:
            r = temp1

        #green
        if tempg < 1.0 / 6.0:
            g = temp1 + (temp2 - temp1) * 6.0 * tempg
        elif tempg < 0.5:
            g = temp2
        elif tempg < 2.0 / 3.0:
            g = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempg) * 6.0
        else:
            g = temp1

        #blue
        if tempb < 1.0 / 6.0:
            b = temp1 + (temp2 - temp1) * 6.0 * tempb
        elif tempb < 0.5:
            b = temp2
        elif tempb < 2.0 / 3.0:
            b = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempb) * 6.0
        else:
            b = temp1

        r *= 255
        g *= 255
        b *= 255
    return [r,g,b]

def hslAndBack(pixel):
    pixelHSL = rgb2hsl(pixel)
    pixelRGB = hsl2rgb(pixelHSL)
    return pixelRGB


def hueShift(pixel):
    hsl = rgb2hsl(pixel)
    r = (hsl[0]+shift)%255
    rgb = hsl2rgb([r, hsl[1], hsl[2]])
    return rgb

def invertColor(pixel):
    return (255-pixel[0], 255-pixel[1], 255-pixel[2])

def redStrip(pixel):
    return [0,pixel[0],pixel[0]]

def greenStrip(pixel):
    return [pixel[0],0,pixel[0]]

def blueStrip(pixel):
    return [pixel[0],pixel[0],0]

def brightAvg(pixel):
    return (pixel[0]+pixel[1]+pixel[2])/3

def brightPerc(pixel):
    return (pixel[0]*.21)+(pixel[1]*.72)+(pixel[2]*.07)

def filterSwitch(mode):
    switch = {
        'avg': brightAvg,
        'perc': brightPerc,
        'invert': invertColor,
        'rstrip': redStrip,
        'gstrip': greenStrip,
        'bstrip': blueStrip,
        'hsl': hslAndBack,
        'hue': hueShift
    }
    func = switch.get(mode, lambda: "Invalid function")
    return func

def filter(array, mode='avg'):
    matrix = []
    for row in array:
        newRow = []
        for elem in row:
            newRow.append(filterSwitch(mode)(elem))
        matrix.append(newRow)
    return matrix

a = filter(a, filterName)
a = np.asarray(a)
newIm = Image.fromarray(a.astype('uint8'))
newIm.show()
