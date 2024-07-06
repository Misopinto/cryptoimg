from PIL import Image
import numpy as np

def imgtoarr(img):
    imag= Image.open(img)
    imgarr= np.asarray(imag)
    return imgarr

def arrtoimg(arr):
    return Image.fromarray(arr)

def file_open(file):
    with open(file,'r') as f:
        return f.readlines()

def strTobin(string):
    binr = ''
    for x in string:
        binr += format(ord(x), '08b')
    return binr

def binTostr(binr):
    num = len(binr)/8 
    string = ''
    for x in range(int(num)):
      start = x*8
      end = (x+1)*8
      string += chr(int(str(binr[start:end]),2))
    return string

if __name__ == "__main__":
    #convert image to array
    arr=imgtoarr("cat_lock.jpg")
    #open the file to encrypt
    file = file_open('secret.txt')[0]
    #convert the file in binary
    binr = strTobin(file)
    #Algorithm
    