'''
Copyright 2013 CyberPoint International, LLC.
All rights reserved. Use and disclosure prohibited
except as permitted in writing by CyberPoint.

libpgm exception handler

Charlie Cabot
Sept 27 2013

'''
class libpgmError(Exception):
    pass

class bntextError(libpgmError):
    pass
