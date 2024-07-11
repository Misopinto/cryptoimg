from cryptoimg_func import arrToimg,encrypt,file_open,imgToarr,reshape,strTobin

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
    #Save the encrypted file as an image
    encrypted_img_path= input('Insert the path where to save the encrypted image: ')
    encrypted_img.save(encrypted_img_path,'PNG')