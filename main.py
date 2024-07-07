from PIL import Image
import numpy as np
import re

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
    #Reshape bin array to match the img array
    bin8 = re.findall('.'*8,binr)
    bin8 = np.array([int(b, 2) for b in bin8], dtype=np.uint8)
    shape_arr = arr.shape[0]*arr.shape[1]*arr.shape[2]
    bin8_fill = np.tile(bin8, shape_arr // bin8.size)
    if bin8_fill.size > shape_arr:
        bin8_fill = bin8_fill[:shape_arr]
    else:
        bin8_fill = np.resize(bin8_fill, shape_arr)
    bin8_resh = bin8_fill.reshape(arr.shape)
    result = bin8_resh * arr
    
    print(result.shape)
    res = arrtoimg(result)
    res.show()
    
    