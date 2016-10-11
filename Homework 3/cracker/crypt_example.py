'''
   This example program simply takes two arguments, a password and a
   salt, and prints the corresponding hash to screen.

   Note that this code should work on any UNIX based OS, including
   Mac OS X, but the behavior of the program is going to differ
   accordingly.


   Also note the behavior on LINUX systems of crypt. The actual
   algorithm to be used is part of the salt. For example, setting the salt to be

   $6$aA349808Abcd$ 

   results in the salt "aA349808Abcd" being used with (iterated)
   SHA-512. The algorithm is controlled by the first number (in this
   case 6). Also refer to the man page of crypt for more information.

   This does not work for example on Mac OS X.
'''
import sys
import crypt

if len(sys.argv) != 3:
    print "Usage: {} password salt".format(sys.argv[0])
else:
    password = sys.argv[1]
    salt = sys.argv[2]

    e_pass = crypt.crypt(password, salt)
    print "Password: {} Salt: {} Hash: {}".format(password, salt, e_pass)