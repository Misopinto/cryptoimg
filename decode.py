from cryptoimg_func import binTostr,decrypt,imgToarr,save_file

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


