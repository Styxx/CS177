#!/usr/bin/env python

__author__ = 'Vincent "Styxx" Chang'

import sys
import logging
import argparse
import crypt
from threading import *

#logger = logging.getLogger(__name__)


### NOTES:

# Straight brute force of words_en.txt:
    # Found targaryend's password
# Replace "i" with "1", "e" with "3", and "o" with "0"
# Replace with all uppercase versions of words_en.txt



def verify(passHash, word, salt, user):

    # we can modify words here to exchange letters numbers, etc
    word = word.upper()
    #word = word.replace("i", "1").replace("e","3").replace("o","0")
    #word = word + "1"

    #DEBUG
    logging.info("[~~] Attempting crack for " + user + ": " + word)    
    
    
    #crypt.crypt(password_guess, $<hashing type>$<salt>$) == $<h>$<salt>$<password hash>

    if len(salt) < 5:
        cryptWord=crypt.crypt(word,salt+passHash)                                  # For DES
        logging.debug("Crypt: " +cryptWord + " || Ours: " +salt+passHash)          # For DES
        if cryptWord == salt+passHash:                                             # For DES
            print "[+++++] Found password for " + user + ": " + word
            logging.info("[+++++] Found password for " + user + ": " + word)
        return
    else:
        cryptWord = crypt.crypt(word, salt)
        logging.debug("Crypt: " +cryptWord + " || Ours: " + salt+"$"+passHash)
        if cryptWord == salt+"$"+passHash:
            print "[+++++] Found password for " + user + ": " + word
            logging.info("[+++++] Found password for " + user + ": " + word)
        return


#t = Thread(target=testPass, args=(passHash, salt, dfile, efile, user))


def testPass(passHash, salt, dfile, user):
    dictFile = open(dfile, 'r')
    
    for word in dictFile.readlines():
        sentword = word.strip('\n')
        if len(sentword) < 6: continue
        #t = Thread(target=testPass2, args=(passHash, salt, dfile, word, user))
        #t = Thread(target=verify, args=(passHash, sentword, salt, user))
        #.start()
        #testPass2(passHash, salt, dfile, word, user)
        
        verify(passHash, sentword, salt, user)
    return



def testPass2(passHash, salt, dfile, word, user):
    dFile2 = open(dfile, 'r')
    for word2 in dFile2.readlines():
        sentword = word+word2
        #t = Thread(target=verify, args=(passHash, sentword, salt, user))
        #t.start()
        if len(sentword) < 6: continue
        verify(passHash, sentword, salt, user)
    return
    


def main():
    
    # Simple argument parsing for files
    parser = argparse.ArgumentParser (
        prog='cracker.py'
    )
    parser.add_argument('-f', '--file', nargs=1, help='password file')      # Shadow file
    parser.add_argument('-d', '--dic', nargs=1, help='dictionary file')     # Dictionary file for brute force
    #parser.add_argument('-e', '--eic', nargs=1, help='dictionary file2')
    args = parser.parse_args()

    if (args.file == None) | (args.dic == None):
        print "Requires password file and dictionary file"
        exit(0)
    else:
        file = args.file[0]
        dfile = args.dic[0]
    #    efile = args.eic[0]
    
    # DEBUG
    #print args
    #print("File: " + file)
    #print("Dfile: " + dfile)
    
    shadowFile = open(file)
    
    # For each user, parse their line in shadow
    for line in shadowFile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            if "$" in line:
                encodeType = line.split(':')[1].split('$')[1]
                saltHash = line.split(':')[1].split('$')[2]
                passHash = line.split(':')[1].split('$')[3]
            else:
                passHash = line.split(':')[1]
                saltHash = passHash[:2]
                passHash = passHash[2:]
                encodeType = "-1"
            
            if encodeType == "-1":
                #salt = "$"+saltHash
                salt = saltHash
            else:
                salt = "$"+encodeType+"$"+saltHash
            
            logging.basicConfig(filename='logger.log', level=logging.DEBUG)
            print "[*] Starting the crack for: "+user
            logging.info("[*] Starting the crack for: "+user)
            
            #t = Thread(target=testPass, args=(passHash, salt, dfile, user))
            #t.start()
            
            
            # DEBUG - Check that shadow parsing is correct
            #print "User: " + user
            #print "Salt: " + salt
            #print "Password hash: " + passHash
            #print "Sending: "+salt+passHash
            
            testPass(passHash, salt, dfile, user)
    
    exit(0)
        



if __name__ == '__main__':
    main()