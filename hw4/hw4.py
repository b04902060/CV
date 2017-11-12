import Image
import numpy as np


def binarize(pic):
    for i in range(512):
        for j in range(512):
            if pic[i][j] > 127:
                pic[i][j] = 255
            else:
                pic[i][j] = 0
    return pic


def dilation(pic, kernel):
    new_pic = np.array(pic)
    for i in range(512):
        for j in range(512):
            if pic[i][j] == 255:
                for k in kernel:
                    if i+k[0]>=0 and j+k[1]>=0:
                        try:
                            new_pic[i+k[0]][j+k[1]] = 255
                        except:
                            pass
    return new_pic


def hit_and_miss(pic):
    k1 = [[0,-1], [1,0]]
    k2 = [[-1,0], [-1,1], [0,1]]
    inside = erosion(pic, k1)
    new_pic = np.array(pic)
    for i in range(512):
        for j in range(512):
            new_pic[i][j] = 0
            try:
                if pic[i-1][j] == 0 and pic[i][j+1] == 0 and pic[i-1][j+1] == 0:
                    if inside[i][j] == 255:
                        new_pic[i][j] = 255
            except:
                pass
    return new_pic
            


def erosion(pic, kernel):
    new_pic = np.array(pic)
    for i in range(512):
        for j in range(512):
            if pic[i][j] == 255:
                flag = 1
                for k in kernel:
                    if i+k[0]>=0 and j+k[1]>=0:
                        try:
                            if pic[i+k[0]][j+k[1]] == 0:
                                flag = 0
                                break
                        except:
                            pass
                if flag == 0:
                    new_pic[i][j] = 0
    return new_pic


def closing(pic, kernel):
    return erosion(dilation(pic, kernel), kernel)

def opening(pic, kernel):
    return dilation(erosion(pic, kernel), kernel)



def main():
    im = Image.open('lena.bmp').convert('L')
    lena = np.array(im)
    
    lena = binarize(lena)
    kernel = [[0,1], [1,0], [-1,0], [0,-1]]

    lena_dilation = dilation(lena, kernel)
    im = Image.fromarray(lena_dilation)
    im.save('lena_dilation.bmp')

    lena_erosion = erosion(lena, kernel)
    im = Image.fromarray(lena_erosion)
    im.save('lena_erosion.bmp')

    lena_open = opening(lena, kernel)
    im = Image.fromarray(lena_open)
    im.save('lena_opening.bmp')

    lena_close = closing(lena, kernel)
    im = Image.fromarray(lena_close)
    im.save('lena_closing.bmp')

    lena_hit = hit_and_miss(lena)
    im = Image.fromarray(lena_hit)
    im.save('lena_hit_and_miss.bmp')


if __name__ == '__main__':
    main()
