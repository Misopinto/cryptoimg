from PIL import Image
import numpy as np
from numpy import random
import base64

def arrToimg(arr):
    #Convert the array to Pillow image
    return Image.fromarray(arr)

def binTostr(binr):
    #converts the binary string to corresponding ASCII string
    num = len(binr) // 8
    decoded_string = ''.join(chr(int(binr[i*8:(i+1)*8], 2)) for i in range(num))
    original_string = decode_string(decoded_string)
    return original_string

def decode_string(encoded_string):
    #Check if input is a string
    if isinstance(encoded_string, str):
        # Ensure the encoded string is byte-aligned by padding with '='
        padding = '=' * ((4 - len(encoded_string) % 4) % 4)
        padded_encoded_string = encoded_string + padding
        #Encode first in utf-8 and then decode in base64 and to utf-8
        byte_data = padded_encoded_string.encode('utf-8')
        decoded_data = base64.b64decode(byte_data)
        decoded_string = decoded_data.decode('utf-8')
        return decoded_string
    else:
        raise ValueError("The input must be a string")
    
def decrypt(encrypted_arr, arr):
    #Generate the random key
    key_img = generate_random_key(arr)
    #Using the bitwise xor function the encrypted array and the key<=>image array are unjoined
    decrypted_arr = np.bitwise_xor(encrypted_arr,key_img)
    #Extract from the last elements of the encrypted array the length of the 8-bit chunks and return them as integers
    len_bin8 = (int(encrypted_arr[-1, -1, -3]) << 16) | (int(encrypted_arr[-1, -1, -2]) << 8) | int(encrypted_arr[-1, -1, -1])
    #Flatten the decrypted array
    bin8_flat = decrypted_arr.flatten()
    #Extract the binary string of the file using the calculated length before it repeats
    bin8_fix = [bin8_flat[i] for i in range(len_bin8)]
    binary = ''.join([format(b, '08b') for b in bin8_fix])
    return binary

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

def file_open(file_path):
    #Opens and reads the file, extracting its contents
    with open(file_path, 'r') as f:
        return f.read()
    
def generate_random_key(img_arr):
    #A seed is generated based on the sum of the image array values
    seed = np.sum(img_arr)
    random.seed(seed)
    #Based on the seed value, a series of values that correspond to the size of the image array is generated, with values ranging from 0 to 256
    key = random.randint(0, 256, size=img_arr.shape, dtype=np.uint8)
    #The image array and the key array are joined using the bitwise xor function
    img_key = np.bitwise_xor(img_arr, key)
    return img_key

def imgToarr(img_path):
    #Open the Image with pillow and convert it to a numpy array
    imag = Image.open(img_path)
    imgarr = np.asarray(imag)
    return imgarr

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

def save_file(name_path,string):
    with open(name_path,'w') as file:
        file.write(string)

def strTobin(string):
    #Convert the String encoded to binary
    encoded_string = encode_string(string)
    binr = ''.join(format(ord(i), '08b') for i in encoded_string)
    return binr