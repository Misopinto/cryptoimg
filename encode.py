import argparse
from cryptoimg_func import arrToimg,encrypt,file_open,imgToarr,reshape,strTobin

parser = argparse.ArgumentParser()
parser.add_argument('-i')
parser.add_argument('-f')
parser.add_argument('-s')

args = parser.parse_args()

def init_path():
    #Get image Path
    img_path = input('Insert image path: ')
    #Get file path
    file_path = input('Insert File path: ')
    encrypted_img_path= input('Insert the path where to save the encrypted image: ')
    return img_path,file_path,encrypted_img_path

def main(img_path,file_path,encrypted_img_path='Encryptedimg'):
    #initialize image as arr
    img = imgToarr(img_path)
    #Read File and convert string to binary
    file = file_open(file_path)
    binary = strTobin(file)
    #Reshape the binary to adapt to image array
    binary_reshaped, binary_byte = reshape(binary,img)
    #Encrypt the file using the image and a pseudorandomic key
    encrypted = encrypt(binary_reshaped,img,binary_byte)
    encrypted_img = arrToimg(encrypted)
    encrypted_img.save(f'{encrypted_img_path}.png','PNG')

if __name__ == '__main__':
    if args.i == None and args.f == None and args.s == None:
        args.i,args.f,args.s = init_path()
    main(args.i,args.f,args.s)