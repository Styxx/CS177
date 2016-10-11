# CS177 -- padding oracle attacks This code is (unfortunately) meant
# to be run with Python 2.7.10 on the CSIL cluster
# machines. Unfortunately, cryptography libraries are not available
# for Python3 at present, it would seem.
from Crypto.Cipher import AES
import binascii
import sys
#import pprint

def check_enc(text):
    nl = len(text)
    val = int(binascii.hexlify(text[-1]), 16)
    if val == 0 or val > 16:
        return False

    for i in range(1,val+1):
        if (int(binascii.hexlify(text[nl-i]), 16) != val):
            return False
    return True


# Returns True if padding is valid. False otherwise
def PadOracle(ciphertext):
    if len(ciphertext) % 16 != 0:
        return False
    
    tkey = 'Sixteen byte key'

    ivd = ciphertext[:AES.block_size]
    dc = AES.new(tkey, AES.MODE_CBC, ivd)
    ptext = dc.decrypt(ciphertext[AES.block_size:])

    return check_enc(ptext)


    
    
# Decrypts any given ciphertext encrypted under key
#   by only using calls to PadOracle

# Padding-oracle attack comes here
def RunAttackOnChunk(block1, block2):
  multiFlag = 0
  
  
  
  # Check second to last byte in block 2 if <= 16
  if block2[14] <= 16:
    print("Multiple possible values")
    multiFlag = 1
    
    
    
  
  if (multiFlag)
    # Stuff
  else:
    guessBit = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    padArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    oldBit = []

    # For every byte in chunk
    for padNumber in range(0, 16):
      breakout = 1
      while (breakout):
        
        # For every byte up till padNumber
        for i in range(0, padNumber):
          # Save old bit in array
          oldBit[i] = block2[-1 - i]
          # XOR and save new bit into array
          newBit = block2[-1 - i] ^ guessBit[i] ^ (padNumber+1)
          block2[-1 - i] = newBit
          
        # Check if padding is correct in new array
        if PadOracle(str(block2)):
          print(str(padNumber+1) + ". Valid with guessBit: " + str(guessBit[padNumber]))
          # Decrement guess bit since we increment it later. Keeps guessBit where it should be
          guessBit[padNumber] = guessBit[padNumber] - 1
          breakout = 0
        
        # Increment guess bit
        guessBit[padNumber] = guessBit[padNumber] + 1
        
        # Reset block to old bits
        for j in range(0, padNumber):
          block[-1 - j] = oldBit[j]
          
          
      """
      while(breakout):
        oldb1 = block2[-1]
        oldb2 = block2[-2]
        oldb3 = block3[-3]
        newb1 = block2[-1] ^ guessBit[0] ^ 2
        newb2 = block2[-2] ^ guessBit[1] ^ 2
        newb3 = block2[-3] ^ guessBit[2] ^ 2
        block2[-1] = newb1
        block2[-2] = newb2
        block2[-3] = newb3
        
        if PadOracle(str(block2)):
          print("1. Valid with guessBit: " + str(guessBit[0])
          guessBit[0] = guessBit[0] - 1
          breakout = 0
          
        # Increment and reset bits
        guessBit[0] = guessBit[0] + 1
        block2[-1] = oldb1
        block2[-2] = oldb2
        block2[-3] = oldb3
      """
      

    
if len(sys.argv) > 1:
    myfile = open(sys.argv[1], "r")
    ctext=myfile.read()
    myfile.close()

    # complete from here. The ciphertext is now (hopefully) stored in
    # ctext as a string. Individual symbols can be accessed as
    # int(ctext[i]). Some more hints will be given on the Piazza
    # page.

    # Array of ints in range 0 ... 255
    cb = bytearray(ctext)
    
    """
    # Split into separate lists
    clist = [cb[i:i+16] for i in xrange(0, len(cb), 16)]

    print("cb:")
    pprint.pprint(cb)
    print("clist:")
    pprint.pprint(clist)
    """
    
    
    print("Stopped here")
    

    # end completing here, leave rest unchanged.
else:
    print("You need to specify a file!")
    
