import argparse
from cryptoimg_func import binTostr,decrypt,imgToarr,save_file

parser = argparse.ArgumentParser()
parser.add_argument('-e')
parser.add_argument('-i')
parser.add_argument('-s')

args = parser.parse_args()

def init_path():
    #Get encrypted file image path
    encrypted_path = input('Insert Encrypted file image path: ')
    #Get the Image path
    img_path = input('Insert Image path: ')
    #Save File
    filepath = input('Insert decrypted file path where to save: ')
    return encrypted_path,img_path,filepath

def main(encrypted_path,img_path,filepath):
    #Convert image to array
    encrypted = imgToarr(encrypted_path)
    #Convert image to array
    img_arr = imgToarr(img_path)
    #Decrypt the File
    binary_file= decrypt(encrypted,img_arr)
    #Convert binary to string
    file = binTostr(binary_file)
    #Save File
    save_file(f'{filepath}.txt',file)

if __name__ == '__main__':
    if args.e == None and args.i == None and args.s == None:
        args.e,args.i,args.s = init_path()
    main(args.e,args.i,args.s)

