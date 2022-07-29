# Name : Shubhay Islaniya 















#importing libararies to be used in the program
from Crypto.Cipher import DES
from Crypto.Hash import SHA256
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
import time
from pyfiglet import Figlet



#time delays has been added as the program instantaenoulsy completes it and the output reult isnt show in suck small time period
#constants of the program 
#just keep define them in the beginning and dont forget to keep b"_your_token_" while defining salt_constnt and pi = yourchoiceidnumber
pi=128
salt_const=b"jdhfaug0ahfuibarrifshubhaygas7u9g^&(^)^^%$%#%$)^)^&^&*^%%$#$#%(^)^"


#defining the fucntions for encryption and decryption 


#defining encryption function
def encryptor(path):
	#opening the image file
	try:
		with open(path, 'rb') as imagefile:
			image=imagefile.read()
			
		#padding	
		while len(image)%8!=0:
			image+=b" "
	except:
		print("Error loading the file, make sure file is in same directory, spelled correctly and non-corrupted")
		time.sleep(5)
		exit()
	
	#hashing original image in SHA256	
	hash_of_original=SHA256.new(data=image)
	
	
	
	#Inputting Keys/password
	key1=getpass(prompt="ENTER 10 CHARACTER PASSWORD:\n")
	#Checking if password is of invalid length
	while len(key1)<10:
		key1=getpass(prompt=" ENTER MORE CHARACTERS THAN 10 FOR VALID PSWD:\n")
	
	key1_confirm=getpass(prompt="ENTER THE PASSWORD AGAIN:\n")
	while key1!=key1_confirm:

		print("PASSWORD MISMATCH ! TRY AGAIN\n")
		key1=getpass(prompt="ENTER 10 CHARACTER LONG PASSWORD:\n")
	
		#Checking if password is of invalid length
		while len(key1)<10:
			key1=getpass(prompt="INVALID PASSWORD\n")
		key1_confirm=getpass(prompt="ENTER THE PASSWORD AGAIN:\n")
	
	
	#Salting and hashing password
	key1=PBKDF2(key1,salt_const,48,count=pi)

	
	#using triple DES encryption to perform the action 	
	print("ENCRYPTING...")	
	try:
		cipher1=DES.new(key1[0:8],DES.MODE_CBC,key1[24:32])
		ciphertext1=cipher1.encrypt(image)
		cipher2=DES.new(key1[8:16],DES.MODE_CBC,key1[32:40])
		ciphertext2=cipher2.decrypt(ciphertext1)
		cipher3=DES.new(key1[16:24],DES.MODE_CBC,key1[40:48])
		ciphertext3=cipher3.encrypt(ciphertext2)
		print("!!!ENCRYPTION SUCCESSFUL!!!")
		time.sleep(5)
		
	except:
		print("ENCRYPTION FAILED")
		time.sleep(5)
		exit()
	
		
	
	#Adding hash at end of encrypted bytes
	ciphertext3+=hash_of_original.digest()

	
	#Saving the file encrypted
	try:
		dpath="encrypted_"+path
		with open(dpath, 'wb') as image_file:
    			image_file.write(ciphertext3)
		print("ENCRYPTED IMAGE/FILE SAVES AS "+dpath)
    		
		
	except:
		temp_path=input("SAVING FILE FAILURE TRY AGAIN")
		try:
			dpath=temp_path+path
			dpath="encrypted_"+path
			with open(dpath, 'wb') as image_file:
    				image_file.write(ciphertext3)
			print(" FILE SAVED SUCCESFULLY AS "+dpath)
			time.sleep(5)
			exit()
		except:
			print("FAILED AND EXITING.......")
			time.sleep(5)
			exit()








#defining decryption fucntion
def decryptor(efile):
	
	try:
		with open(efile,'rb') as encrypted_file:
			encrypted_data_with_hash=encrypted_file.read()
			
	except:
		print("UNABLE TO READ CHECK IF ITS IN DIRECTORY ")
		time.sleep(5)
		exit()
	
	
	#Inputting the password
	key_dec=getpass(prompt="ENTER PASSWORD:\n")
	
	
	#extracting hash and cipher data without hash
	extracted_hash=encrypted_data_with_hash[-32:]
	encrypted_data=encrypted_data_with_hash[:-32]

	
	#salting and hashing password
	key_dec=PBKDF2(key_dec,salt_const,48,count=pi)
	

	#decrypting using triple 3 key DES
	#CBC = cipher bloc  k chaining
	print("DECRYPTING......")
	try:
		
		cipher1=DES.new(key_dec[16:24],DES.MODE_CBC,key_dec[40:48])
		plaintext1=cipher1.decrypt(encrypted_data)
		cipher2=DES.new(key_dec[8:16],DES.MODE_CBC,key_dec[32:40])
		plaintext2=cipher2.encrypt(plaintext1)
		cipher3=DES.new(key_dec[0:8],DES.MODE_CBC,key_dec[24:32])
		plaintext3=cipher3.decrypt(plaintext2)
		
		
	except:
		print("DECRYPTION FAILED PLS CHECK LIBARARIES AND INSTALL IF NOT PRESENT")
		
	
	
	
	
	#hashing decrypted plain text
	hash_of_decrypted=SHA256.new(data=plaintext3)

	
	#matching hashes
	if hash_of_decrypted.digest()==extracted_hash:
		print("CORRECT PASSWORD!!!")
		print("DECRYPTION SUCCESSFUL!!!")
		time.sleep(5)
	else:
		print("INCORRECT PASSWORD exiting......!!!")
		time.sleep(5)
		exit()
		4
		
		
	#saving of decrypted files/image
	try:
		epath=efile
		if epath[:10]=="encrypted_":
			epath=epath[10:]
		epath="decrypted_"+epath
		with open(epath, 'wb') as image_file:
			image_file.write(plaintext3)
		print("IMAGE SAVED SUCCESFULLY WITH PATH " + epath)
		print("			Note: If the decrypted image is appearing to be corrupted then password may be wrong or it may be file format error")
		time.sleep(5)
	except:
		temp_path=input("			Saving file failed!. Enter alternate name without format to save the decrypted file. If it is still failing then check system memory")
		time.sleep(5)
		try:
			epath=temp_path+efile
			with open(epath, 'wb') as image_file:
				image_file.write(plaintext3)
			print("Image saved successully with name " + epath)
			print("IF CORRUPTED FILE THEN PASSWORD MAYBE WRONG OR FILE ERROR MUST HAVE OCCURED ")
			time.sleep(5)
		except:
			print("FAILED EXITING.....")
			time.sleep(5)
			exit()





















#main program

print(r"""
 _____                             _             
| ____|_ __   ___ _ __ _   _ _ __ | |_ ___  _ __ 
|  _| | '_ \ / __| '__| | | | '_ \| __/ _ \| '__|
| |___| | | | (__| |  | |_| | |_) | || (_) | |   
|_____|_| |_|\___|_|   \__, | .__/ \__\___/|_|   
                       |___/|_|  """)


	   

try:  
	   
	   print(" \n \n ---------------- | welcome to encryptor | ---------------- \n \n \n \n \n")
	   print (" Prerequistites before using the program \n 1.Install Pycryptodome using pip \n 2.the file/image to be encrypted or to be decrypted should be in the same folder as the program to work \n 3.please remember the key you enter or decryption will fail \n \n \n \n \n ")
	   choice=int(input(" \nTYPE 1 FOR ENCRYPTION \nTYPE 2 FOR DECRYPTION\n \nselect a option:"))
	   while choice !=1 and choice !=2:
	         choice = int(input("invalid choice pls select from above only and try again:"))
except:
	   print("Error,please provide valid output")
	   time.sleep(5)
	   exit()


if choice == 1:
	path = input("enter the imagename.filetype for encryption:\n")
	encryptor(path)
else:
	efile=input("enter the path of imagename.filetype for decryption:\n")
	decryptor(efile)






