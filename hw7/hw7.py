import Image
import numpy as np
import sys


def save_img(array, filename):
    im = Image.fromarray(array)
    im.save(filename)

def padding(lena):
    lena = np.concatenate((np.zeros((64,1), dtype=np.uint8), lena), axis=1)
    lena = np.concatenate((lena, (np.zeros((64,1), dtype=np.uint8))), axis=1)
    lena = np.concatenate((np.zeros((1,66), dtype=np.uint8), lena), axis=0)
    lena = np.concatenate((lena, (np.zeros((1,66), dtype=np.uint8))), axis=0)
    return lena


def yokoi(im):
    im = padding(im)
    array = np.zeros((64,64), dtype=np.int)

    for i in range(64):
        for j in range(64):
            if im[i+1][j+1] == 0:
                array[i][j] = 0
            else:
                array[i][j] = x(im[0+i:3+i, 0+j:3+j])
    return array    


def x(nine):
    a1 = h2(nine[1][2], nine[0][2], nine[0][1])
    a2 = h2(nine[0][1], nine[0][0], nine[1][0])
    a3 = h2(nine[1][0], nine[2][0], nine[2][1])
    a4 = h2(nine[2][1], nine[2][2], nine[1][2])
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


def h2(x1, x6, x2):
    if x1==255 and x6==255 and x2==255:
        return 'r'
    elif x1==255:
        return 'q'
    else:
        return 's'


def interior(arr, kernel): # arr has already been padded
    b_i = np.zeros((64,64), dtype=np.uint8) # default: 0 when neither border nor interior
    for i in range(64):
        for j in range(64):
            if arr[i+1][j+1] == 255:
                flag = 0
                for k in kernel:
                    if arr[i+k[0]+1][j+k[1]+1] != 255:
                        flag = 1
                if flag == 0:
                    b_i[i][j] = 2 # interior 2
                else:
                    b_i[i][j] = 1 # border 1
    return b_i



def marked(interior, kernel): # interior has been padded
    marked_im = np.zeros((64,64), dtype=np.uint8)
    for i in range(64):
        for j in range(64):
            flag = 0
            if interior[i+1][j+1] != 1:
                continue
            for k in kernel:
                if interior[i+k[0]+1][j+k[1]+1] == 2:
                    flag = 1
                    break
            if flag == 1:
                marked_im[i][j] = 1
    return marked_im
                    


def thin(origin, kernel):
    interior_im = interior(padding(origin), kernel)
    marked_im = marked(padding(interior_im), kernel)   

    thin_im = np.array(origin)
    origin = padding(origin)
    flag = 1
    c = 1
    while(flag):
        flag = 0
        interior_im = interior(origin, kernel)
        marked_im = marked(padding(interior_im), kernel)

        for i in range(64):
            for j in range(64):
                if origin[i+1][j+1] == 255:
                    if f(origin[0+i:3+i, 0+j:3+j]) == 1: # removable
                        if marked_im[i][j] == 1: # is marked
                            thin_im[i][j] = 0
                            origin[i+1][j+1] = 0
                            flag = 1
        #save_img(thin_im, 'thin'+str(c)+'.bmp')
        #c = c+1
    return thin_im

def f(nine):
    a1 = h(nine[1][1], nine[1][2], nine[0][2], nine[0][1])
    a2 = h(nine[1][1], nine[0][1], nine[0][0], nine[1][0])
    a3 = h(nine[1][1], nine[1][0], nine[2][0], nine[2][1])
    a4 = h(nine[1][1], nine[2][1], nine[2][2], nine[1][2])
    #print str(a1)+str(a2)+str(a3)+str(a4)
    if a1+a2+a3+a4 == 1:
        return 1
    else:
        return 0

def h(b, c, d, e):
    if b==c and (b!=d or b!=e):
        return 1
    return 0

def main():
    
    kernel = [[0,1],[0,-1],[1,0],[-1,0]]
    kernel = [[0,1],[0,-1],[1,0],[-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]
    im = Image.open('lena_downsample.bmp').convert('L')
    lena = np.array(im)

    
    #im = Image.open('lena_downsample.bmp').convert('L')
    #lena = np.array(im)
    
    # zero padding
    thin_im = thin(lena, kernel)
    yokoi_im = yokoi(lena)


    for i in range(64):
        for j in range(64):
            if thin_im[i][j] == 255:
                sys.stdout.write('*')
                continue
            if yokoi_im[i][j] == 0:
                sys.stdout.write(' ')
            else:
                sys.stdout.write(str(yokoi_im[i][j]))
        print ''
    


if __name__ == '__main__':
    main()
