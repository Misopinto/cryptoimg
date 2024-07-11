from PIL import Image
import numpy as np
from numpy import random
import base64

def encode_string(input_string):
    #Check if input is a string
    if isinstance(input_string, str):
        #Encode first in utf-8, then in base64 and then decode to utf-8
        byte_data = input_string.encode('utf-8')
        encoded_data = base64.b64encode(byte_data)
        encoded_string = encoded_data.decode('utf-8')
        return encoded_string
    else:
        raise ValueError("The input must be a string")

def imgToarr(img_path):
    #Convert the image to a numpy array
    imag = Image.open(img_path)
    imgarr = np.asarray(imag)
    return imgarr

def arrToimg(arr):
    #Convert the array to Pillow image
    return Image.fromarray(arr)

def file_open(file_path):
    #Opens and reads the file, extracting its contents
    with open(file_path, 'r') as f:
        return f.read()

def strTobin(string):
    #Convert the String encoded to binary
    encoded_string = encode_string(string)
    binr = ''.join(format(ord(i), '08b') for i in encoded_string)
    return binr

def reshape(binr, img_arr):
    #Reshape the binary string to adapt to the image array
    #Splitting the binary string to 8-bit chuncks
    bin8 = [binr[i:i+8] for i in range(0, len(binr), 8)]
    #Converting the 8-bit chuncks to integers
    bin8 = np.array([int(b, 2) for b in bin8], dtype=np.uint8)
    #calculating the array size of the image
    shape_arr = img_arr.shape[0] * img_arr.shape[1] * img_arr.shape[2]
    #Repeat the bin8 array enough times to match or exceed the size of the image array
    bin8_fill = np.tile(bin8, shape_arr // bin8.size)
    #If bin8 is larger than necessary, it is cut to the exact size
    if bin8_fill.size > shape_arr:
        bin8_fill = bin8_fill[:shape_arr]
    else:
        bin8_fill = np.resize(bin8_fill, shape_arr)
    #The bin8_fill is reshaped to the same size of the image array
    bin8_resh = bin8_fill.reshape(img_arr.shape)
    return bin8_resh, bin8

def generate_random_key(img_arr):
    #A seed is generated based on the sum of the image array values
    seed = np.sum(img_arr)
    random.seed(seed)
    #Based on the seed value, a series of values that correspond to the size of the image array is generated, with values ranging from 0 to 256
    key = random.randint(0, 256, size=img_arr.shape, dtype=np.uint8)
    #The image array and the key array are joined using the bitwise xor function
    img_key = np.bitwise_xor(img_arr, key)
    return img_key

def encrypt(bin_resh, img_arr ,bin_byte):
    #Generate the random key
    key_img = generate_random_key(img_arr)
    #Using the bitwise xor function the reshaped file and the key<=>image array are joined
    encrypted_arr = np.bitwise_xor(bin_resh,key_img)
    #In the last elements of the encrypted array (which are not significant) is written the length of the 8-bit chunks useful for decryption
    #The length of the 8-bit chuncks are encoded with values in the range from 0 to 256 because of the numpy.uint8 array type
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

