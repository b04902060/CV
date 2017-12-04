import sys, os, math, random
from PIL import Image, ImageDraw
import numpy as np

BLACK = 0
WHITE = 255

I_W = 512
I_H = 512

# n = no value, others are kernal value which range is 0~255
octogon = [
    ['n', 0 , 0 , 0 ,'n'],
    [ 0 , 0 , 0 , 0 , 0 ],
    [ 0 , 0 , 0 , 0 , 0 ],
    [ 0 , 0 , 0 , 0 , 0 ],
    ['n', 0 , 0 , 0 ,'n']
]

class Kernel(object):
    def __init__(self, origin, pattern):
        points = [] #store all points relative to origin
        for y in xrange( len(pattern) ):
            for x in xrange( len(pattern[ 0 ]) ):
                # reverse matrix x and y
                if(pattern[y][x] != 'n'):
                    points.append(( x-origin[0],y-origin[1], pattern[y][x] ))
        self.points = points

    def getPoints(self):
        # get all points in (x,y,value)
        return self.points

def dilation( image, kernel ):
    imageW = I_W
    imageH = I_H
    dilationImage = np.array(image)

    for row in xrange(imageH):
        for col in xrange(imageW):
            originalPixel = image.getpixel((row, col))
            localMax = 0
            for point in kernel.getPoints():
                # edge detect
                if( row+point[0]>=0 and row+point[0]<imageH and col+point[1]>=0 and col+point[1]<imageW ):
                    localMax = max( localMax, image.getpixel((row+point[0],col+point[1])) )
            dilationImage[row, col] = localMax

    return Image.fromarray(dilationImage)

def erosion( image, kernel ):
    imageW = I_W
    imageH = I_H
    erosionImage = np.array(image)

    for row in xrange(imageH):
        for col in xrange(imageW):
            originalPixel = image.getpixel((row, col))
            vaildate = True
            localMin = 255
            for point in kernel.getPoints():
                if( row+point[0]>=0 and row+point[0]<imageH and col+point[1]>=0 and col+point[1]<imageW ):
                    localMin = min( localMin, image.getpixel((row+point[0],col+point[1])) )
            erosionImage[row, col] = localMin

    return Image.fromarray(erosionImage)

def opening( image, kernel ):
    return dilation( erosion(image, kernel), kernel )

def closing( image, kernel ):
    return erosion( dilation(image, kernel), kernel )

def closingThenOpening( image, kernal):
    return opening( closing(image, kernal), kernal )

def openingThenClosing( image, kernal):
    return closing( opening(image, kernal), kernal )

def gaussianNoice( image, amplitude ):
    gaussianImage = np.array(image)
    imageH = I_H
    imageW = I_W
    for row in xrange(imageH):
        for col in xrange(imageW):
            noiseValue = gaussianImage[row, col] + amplitude*random.gauss(0,1)
            if noiseValue > WHITE :
                noiseValue = WHITE
                
            gaussianImage[row, col] = noiseValue

    return Image.fromarray(gaussianImage)

def saltAndPepper( image, threshold ):
    saltImage = np.array(image)
    imageW = I_H
    imageH = I_W

    for row in xrange(imageH):
        for col in xrange(imageW):
            randomValue = random.uniform(0,1)
            if randomValue < threshold :
                saltImage[ row, col ] = BLACK
            elif randomValue > 1-threshold :
                saltImage[ row, col ] = WHITE

    return Image.fromarray(saltImage)


# Use all weight 1 as simple box
def boxFilter( image, boxHeight, boxWidth ):
    filteredImage = np.array(image)
    imageW = I_W
    imageH = I_H

    for row in xrange(imageH):
        for col in xrange(imageW):
            boxList = []
            localOrigin = ( row-(boxHeight/2), col-(boxWidth/2) )
            for boxRow in xrange(boxHeight):
                for boxCol in xrange(boxWidth):
                    x = localOrigin[0]+boxRow
                    y = localOrigin[1]+boxCol
                    if x>=0 and x<imageH and y>=0 and y<imageW:
                        boxList.append(filteredImage[x, y])

            filteredImage[row, col] = sum(boxList)/len(boxList)

    return Image.fromarray(filteredImage)


def median(list):
    half = len(list) / 2
    list.sort()
    if len(list) % 2 == 0:
        return (list[half-1] + list[half])/2
    else:
        return list[half]

def medianFilter( image, boxWidth, boxHeight ):
    filteredImage = np.array(image)
    imageW = I_W
    imageH = I_H

    for row in xrange(imageH):
        for col in xrange(imageW):
            boxList = []
            localOrigin = ( row-(boxHeight/2), col-(boxWidth/2) )
            for boxRow in xrange(boxHeight):
                for boxCol in xrange(boxWidth):
                    x = localOrigin[0]+boxRow
                    y = localOrigin[1]+boxCol
                    if x>=0 and x<imageH and y>=0 and y<imageW:
                        boxList.append(filteredImage[x, y])

            filteredImage[row, col] = median(boxList)

    return Image.fromarray(filteredImage)

def SNR( originImage, noiseImage ):
    imageW = I_W
    imageH = I_H
    size = imageW*imageH
    originPixel = np.array(originImage, dtype=np.float32)
    noisePixel = np.array(noiseImage, dtype=np.float32)
    us = 0
    vs = 0
    un = 0
    vn = 0

    for row in xrange(imageH):
        for col in xrange(imageW):
            us += originPixel[row, col]
    us /= size

    for row in xrange(imageH):
        for col in xrange(imageW):
            vs += math.pow( originPixel[row, col]-us, 2 )
    vs /= size

    for row in xrange(imageH):
        for col in xrange(imageW):
            un += noisePixel[row, col]-originPixel[row, col]
    un /= size

    for row in xrange(imageH):
        for col in xrange(imageW):
            vn += math.pow( noisePixel[row, col]-originPixel[row, col]-un, 2 )
    vn /= size

    return 20*math.log( math.sqrt(vs)/math.sqrt(vn), 10 )

def main():
    im = Image.open("lena.bmp").convert('L')

    octogonKernel = Kernel( (2,2), octogon ) 
    
    # generate noise image
    gaussian_10_Image = gaussianNoice( im, 10 )
    gaussian_30_Image = gaussianNoice( im, 30 )
    gaussian_10_Image.save('gaussian_10_Image.bmp')
    gaussian_30_Image.save('gaussian_30_Image.bmp')
    
    salt_005_Image = saltAndPepper( im, 0.05 )
    salt_01_Image = saltAndPepper( im, 0.1 )
    salt_005_Image.save('salt_005_Image.bmp')
    salt_01_Image.save('salt_01_Image.bmp')

    
    # box3x3
    box3x3_gaussian_10 = boxFilter( gaussian_10_Image, 3, 3)
    box3x3_gaussian_30 = boxFilter( gaussian_30_Image, 3, 3)
    box3x3_salt_005 = boxFilter( salt_005_Image, 3, 3)
    box3x3_salt_01 = boxFilter( salt_01_Image, 3, 3)
    
    box3x3_gaussian_10.save("box3x3_gaussian_10.bmp")
    box3x3_gaussian_30.save("box3x3_gaussian_30.bmp")
    box3x3_salt_005.save("box3x3_salt_005.bmp")
    box3x3_salt_01.save("box3x3_salt_01.bmp")

    # box5x5
    box5x5_gaussian_10 = boxFilter( gaussian_10_Image, 5, 5)
    box5x5_gaussian_30 = boxFilter( gaussian_30_Image, 5, 5)
    box5x5_salt_005 = boxFilter( salt_005_Image, 5, 5)
    box5x5_salt_01 = boxFilter( salt_01_Image, 5, 5)

    box5x5_gaussian_10.save("box5x5_gaussian_10.bmp")
    box5x5_gaussian_30.save("box5x5_gaussian_30.bmp")
    box5x5_salt_005.save("box5x5_salt_005.bmp")
    box5x5_salt_01.save("box5x5_salt_01.bmp")

    #median3x3
    median3x3_gaussian_10 = medianFilter( gaussian_10_Image, 3, 3)
    median3x3_gaussian_30 = medianFilter( gaussian_30_Image, 3, 3)
    median3x3_salt_005 = medianFilter(salt_005_Image, 3, 3)
    median3x3_salt_01 = medianFilter(salt_01_Image, 3, 3)

    median3x3_gaussian_10.save("median3x3_gaussian_10.bmp")
    median3x3_gaussian_30.save("median3x3_gaussian_30.bmp")
    median3x3_salt_005.save("median3x3_salt_005.bmp")
    median3x3_salt_01.save("median3x3_salt_01.bmp")
    
    #median5x5
    median5x5_gaussian_10 = medianFilter( gaussian_10_Image, 5, 5)
    median5x5_gaussian_30 = medianFilter( gaussian_30_Image, 5, 5)
    median5x5_salt_005 = medianFilter(salt_005_Image, 5, 5)
    median5x5_salt_01 = medianFilter(salt_01_Image, 5, 5)

    median5x5_gaussian_10.save("median5x5_gaussian_10.bmp")
    median5x5_gaussian_30.save("median5x5_gaussian_30.bmp")
    median5x5_salt_005.save("median5x5_salt_005.bmp")
    median5x5_salt_01.save("median5x5_salt_01.bmp")
    

    # closing then opening
    closingThenOpening_gaussian_10 = closingThenOpening( gaussian_10_Image, octogonKernel)
    closingThenOpening_gaussian_30 = closingThenOpening( gaussian_30_Image, octogonKernel)
    closingThenOpening_salt_005 = closingThenOpening( salt_005_Image, octogonKernel)
    closingThenOpening_salt_01 = closingThenOpening( salt_01_Image, octogonKernel)

    closingThenOpening_gaussian_10.save("closingThenOpening_gaussian_10.bmp")
    closingThenOpening_gaussian_30.save("closingThenOpening_gaussian_30.bmp")
    closingThenOpening_salt_005.save("closingThenOpening_salt_005.bmp")
    closingThenOpening_salt_01.save("closingThenOpening_salt_01.bmp")
    

    # opening then closing
    openingThenClosing_gaussian_10 = openingThenClosing( gaussian_10_Image, octogonKernel)
    openingThenClosing_gaussian_30 = openingThenClosing( gaussian_30_Image, octogonKernel)
    openingThenClosing_salt_005 = openingThenClosing( salt_005_Image, octogonKernel)
    openingThenClosing_salt_01 = openingThenClosing( salt_01_Image, octogonKernel)

    openingThenClosing_gaussian_10.save("openingThenClosing_gaussian_10.bmp")
    openingThenClosing_gaussian_30.save("openingThenClosing_gaussian_30.bmp")
    openingThenClosing_salt_005.save("openingThenClosing_salt_005.bmp")
    openingThenClosing_salt_01.save("openingThenClosing_salt_01.bmp")
    


    file = open("SNR.txt", "w")

    file.write( "box3x3_gaussian_10: "+ str(SNR(im, box3x3_gaussian_10)) + '\n' )
    file.write( "box3x3_gaussian_30: "+ str(SNR(im, box3x3_gaussian_30)) + '\n' )
    file.write( "box3x3_salt_005: "+ str(SNR(im, box3x3_salt_005)) + '\n' )
    file.write( "box3x3_salt_01: "+ str(SNR(im, box3x3_salt_01)) + '\n' )


    file.write( "box5x5_gaussian_10: "+ str(SNR(im, box5x5_gaussian_10)) + '\n' )
    file.write( "box5x5_gaussian_30: "+ str(SNR(im, box5x5_gaussian_30)) + '\n' )
    file.write( "box5x5_salt_005: "+ str(SNR(im, box5x5_salt_005)) + '\n' )
    file.write( "box5x5_salt_01: "+ str(SNR(im, box5x5_salt_01)) + '\n' )
    
    file.write( "median3x3_gaussian_10: "+ str(SNR(im, median3x3_gaussian_10)) + '\n' )
    file.write( "median3x3_gaussian_30: "+ str(SNR(im, median3x3_gaussian_30)) + '\n' )
    file.write( "median3x3_salt_005: "+ str(SNR(im, median3x3_salt_005)) + '\n' )
    file.write( "median3x3_salt_01: "+ str(SNR(im, median3x3_salt_01)) + '\n' )

    file.write( "median5x5_gaussian_10: "+ str(SNR(im, median5x5_gaussian_10)) + '\n' )
    file.write( "median5x5_gaussian_30: "+ str(SNR(im, median5x5_gaussian_30)) + '\n' )
    file.write( "median5x5_salt_005: "+ str(SNR(im, median5x5_salt_005)) + '\n' )
    file.write( "median5x5_salt_01: "+ str(SNR(im, median5x5_salt_01)) + '\n' )    

    file.write( "closingThenOpening_gaussian_10: "+ str(SNR(im, closingThenOpening_gaussian_10)) + '\n' )
    file.write( "closingThenOpening_gaussian_30: "+ str(SNR(im, closingThenOpening_gaussian_30)) + '\n' )
    file.write( "closingThenOpening_salt_005: "+ str(SNR(im, closingThenOpening_salt_005)) + '\n' )
    file.write( "closingThenOpening_salt_01: "+ str(SNR(im, closingThenOpening_salt_01)) + '\n' )

    file.write( "openingThenClosing_gaussian_10: "+ str(SNR(im, openingThenClosing_gaussian_10)) + '\n' )
    file.write( "openingThenClosing_gaussian_30: "+ str(SNR(im, openingThenClosing_gaussian_30)) + '\n' )
    file.write( "openingThenClosing_salt_005: "+ str(SNR(im, openingThenClosing_salt_005)) + '\n' )
    file.write( "openingThenClosing_salt_01: "+ str(SNR(im, openingThenClosing_salt_01)) + '\n' )

if __name__ == '__main__':
    main()

   

# reference: https://github.com/LucienLee/CV-Homework-in-Python/blob/master/hw8