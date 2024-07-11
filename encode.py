from PIL import Image
import numpy as np
from numpy import random
import base64

def encode_string(input_string):
    if isinstance(input_string, str):
        byte_data = input_string.encode('utf-8')
        encoded_data = base64.b64encode(byte_data)
        encoded_string = encoded_data.decode('utf-8')
        return encoded_string
    else:
        raise ValueError("L'input deve essere una stringa")

def imgToarr(img_path):
    imag = Image.open(img_path)
    imgarr = np.asarray(imag)
    return imgarr

def arrToimg(arr):
    return Image.fromarray(arr)

def file_open(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def strTobin(string):
    encoded_string = encode_string(string)
    binr = ''.join(format(ord(i), '08b') for i in encoded_string)
    return binr

def reshape(binr, img_arr):
    bin8 = [binr[i:i+8] for i in range(0, len(binr), 8)]
    bin8 = np.array([int(b, 2) for b in bin8], dtype=np.uint8)
    shape_arr = img_arr.shape[0] * img_arr.shape[1] * img_arr.shape[2]
    bin8_fill = np.tile(bin8, shape_arr // bin8.size)
    if bin8_fill.size > shape_arr:
        bin8_fill = bin8_fill[:shape_arr]
    else:
        bin8_fill = np.resize(bin8_fill, shape_arr)
    bin8_resh = bin8_fill.reshape(img_arr.shape)
    return bin8_resh, bin8

def generate_random_key(arr):
    seed = np.sum(arr)
    random.seed(seed)
    return random.randint(0, 256, size=arr.shape, dtype=np.uint8)

def img_key(arr, key):
    img_key = np.bitwise_xor(arr, key)
    return img_key

def encrypt(bin_resh, img_arr ,bin_byte):
    key = generate_random_key(img_arr)
    key_img = img_key(img_arr, key)
    encrypted_arr = np.bitwise_xor(bin_resh,key_img)
    encrypted_arr[-1, -1, -3] = (len(bin_byte) >> 16) & 0xFF
    encrypted_arr[-1, -1, -2] = (len(bin_byte) >> 8) & 0xFF
    encrypted_arr[-1, -1, -1] = len(bin_byte) & 0xFF
    return encrypted_arr

if __name__ == '__main__':
    #Get image Path
    img_path = input('Insert image path: ')
    #initialize image as arr
    img = imgToarr(img_path)
    #Get file path
    file_path = input('Insert File path: ')
    #Read File and convert string to binary
    file = file_open(file_path)
    binary = strTobin(file)
    #Reshape the binary to adapt to image array
    binary_reshaped, binary_byte = reshape(binary,img)
    #Encrypt the file using the image and a pseudorandomic key
    encrypted = encrypt(binary_reshaped,img,binary_byte)
    encrypted_img = arrToimg(encrypted)
    encrypted_img.save('encrypted_img1.png','PNG')
    encrypted_img.show()

