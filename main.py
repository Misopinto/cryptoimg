from PIL import Image
import numpy as np

def imgtoarr(img):
    imag= Image.open(img)
    imgarr= np.asarray(imag)
    return imgarr

def arrtoimg(arr):
    return Image.fromarray(arr)

if __name__ == "__main__":
    arr=imgtoarr("cat_lock.jpg")
    print(arr)
    img= arrtoimg(arr)
    img.show()