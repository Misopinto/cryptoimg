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

def decode_string(encoded_string):
    if isinstance(encoded_string, str):
        # Ensure the encoded string is byte-aligned by padding with '='
        padding = '=' * ((4 - len(encoded_string) % 4) % 4)
        padded_encoded_string = encoded_string + padding
        
        byte_data = padded_encoded_string.encode('utf-8')
        decoded_data = base64.b64decode(byte_data)
        decoded_string = decoded_data.decode('utf-8')
        return decoded_string
    else:
        raise ValueError("L'input deve essere una stringa")

def imgToarr(img_path):
    imag = Image.open(img_path)
    imgarr = np.asarray(imag)
    return imgarr

def binTostr(binr):
    num = len(binr) // 8
    decoded_string = ''.join(chr(int(binr[i*8:(i+1)*8], 2)) for i in range(num))
    original_string = decode_string(decoded_string)
    return original_string

def generate_random_key(arr):
    seed = np.sum(arr)
    random.seed(seed)
    return random.randint(0, 256, size=arr.shape, dtype=np.uint8)

def img_key(arr, key):
    img_key = np.bitwise_xor(arr, key)
    return img_key

def decrypt(encrypted_arr, arr):
    key = generate_random_key(arr)
    key_img = img_key(arr, key)
    decrypted_arr = np.bitwise_xor(encrypted_arr,key_img)
    len_bin8 = (int(encrypted_arr[-1, -1, -3]) << 16) | (int(encrypted_arr[-1, -1, -2]) << 8) | int(encrypted_arr[-1, -1, -1])
    bin8_flat = decrypted_arr.flatten()
    bin8_fix = [bin8_flat[i] for i in range(len_bin8)]
    binary = ''.join([format(b, '08b') for b in bin8_fix])
    return binary

def save_file(name_path,string):
    with open(name_path,'w') as file:
        file.write(string)

if __name__ == '__main__':
    #Get encrypted file image path
    encrypted_path = input('Insert Encrypted file image path: ')
    #Convert image to array
    encrypted = imgToarr(encrypted_path)
    #Get the Image path
    img_path = input('Insert Image path: ')
    #Convert image to array
    img_arr = imgToarr(img_path)
    #Decrypt the File
    binary_file= decrypt(encrypted,img_arr)
    #Convert binary to string
    file = binTostr(binary_file)
    #Save File
    filepath = input('Insert decrypted file path where to save: ')
    save_file(filepath,file)


