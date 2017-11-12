import Image
import numpy as np


def dilation(pic, kernel):
    new_pic = np.array(pic)
    for i in range(512):
        for j in range(512):
            for r,c in kernel:
                try:
                    if new_pic[i][j] < pic[i+r][j+c]:
                        new_pic[i][j] = pic[i+r][j+c]
                except:
                    pass
    return new_pic



def erosion(pic, kernel):
    new_pic = np.array(pic)
    for i in range(512):
        for j in range(512):
            for r,c in kernel:
                try:
                    if new_pic[i][j] > pic[i+r][j+c]:
                        new_pic[i][j] = pic[i+r][j+c]
                except:
                    pass
    return new_pic


def closing(pic, kernel):
    return erosion(dilation(pic, kernel), kernel)

def opening(pic, kernel):
    return dilation(erosion(pic, kernel), kernel)



def main():
    im = Image.open('lena.bmp').convert('L')
    lena = np.array(im)
    
    
    kernel = [[-2,-1],[-2,0],[-2,1],  [-1,-2],[-1,-1],[-1,0],[-1,1],[-1,2],  [0,-2],[0,-1],[0,0],[0,1],[0,2],  [1,-2],[1,-1],[1,0],[1,1],[1,2],  [2,-1],[2,0],[2,1]]

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



if __name__ == '__main__':
    main()
