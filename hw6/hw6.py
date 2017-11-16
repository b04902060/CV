import Image
import numpy as np
import sys

def downsample(im):
    new_im = np.zeros((64,64), dtype=np.uint8)
    for i in range(64):
        for j in range(64):
            new_im[i][j] = im[i*8][j*8]
    return new_im

def binarize(pic):
    for i in range(64):
        for j in range(64):
            if pic[i][j] > 127:
                pic[i][j] = 255
            else:
                pic[i][j] = 0
    return pic

def save_img(array, filename):
    im = Image.fromarray(array)
    im.save(filename)


def yokoi(im):
    array = np.zeros((64,64), dtype=np.int)

    for i in range(64):
        for j in range(64):
            if im[i+1][j+1] == 0:
                array[i][j] = 0
            else:
                array[i][j] = x(im[0+i:3+i, 0+j:3+j])
    return array


def x(nine):
    a1 = h(nine[1][2], nine[0][2], nine[0][1])
    a2 = h(nine[0][1], nine[0][0], nine[1][0])
    a3 = h(nine[1][0], nine[2][0], nine[2][1])
    a4 = h(nine[2][1], nine[2][2], nine[1][2])
    if a1=='r' and a2=='r' and a3=='r' and a4=='r':
        return 5
    else: # this is very stupid...
        count = 0
        if a1 =='q':
            count = count+1
        if a2 =='q':
            count = count+1
        if a3 =='q':
            count = count+1
        if a4 =='q':
            count = count+1
        return count


def h(x1, x6, x2):
    if x1==255 and x6==255 and x2==255:
        return 'r'
    elif x1==255:
        return 'q'
    else:
        return 's'

def main():
    
    
    im = Image.open('lena.bmp').convert('L')
    lena = np.array(im)
    lena = downsample(lena)
    lena = binarize(lena)
    save_img(lena, 'lena_downsample.bmp')
    

    
    #im = Image.open('lena_downsample.bmp').convert('L')
    #lena = np.array(im)
    
    # zero padding
    lena = np.concatenate((np.zeros((64,1), dtype=np.uint8), lena), axis=1)
    lena = np.concatenate((lena, (np.zeros((64,1), dtype=np.uint8))), axis=1)
    lena = np.concatenate((np.zeros((1,66), dtype=np.uint8), lena), axis=0)
    lena = np.concatenate((lena, (np.zeros((1,66), dtype=np.uint8))), axis=0)

    output = yokoi(lena)

    for i in range(64):
        for j in range(64):
            if output[i][j] == 0:
                sys.stdout.write(' ')
            else:
                sys.stdout.write(str(output[i][j]))
        print ''



if __name__ == '__main__':
    main()
