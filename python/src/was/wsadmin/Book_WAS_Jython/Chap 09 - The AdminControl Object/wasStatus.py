#---------------------------------------------------------------------
#  Name: wasStatus.py
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Python script used to display the status of all application
#        servers in the cell.
#*********************************************************************
#  Note: This is not a wsadmin script, it is a Python script, and
#        requires a Python interpreter be installed in order to be
#        used.
#*********************************************************************
#   Usage: python wasStatus.py <WAS_HOME>
# Example: python wasStatus.py C:\IBM\WebSphere\AppServer
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/01 0.0 rag New - written to simplify wsadmin script testing
#---------------------------------------------------------------------
import sys, re

#---------------------------------------------------------------------
# Name: WSASstatus()
# Role: Identify the existing profiles, and get the status for each
#       AppServer therein
#---------------------------------------------------------------------
def WSASstatus() :
  import os

  #-------------------------------------------------------------------
  # How many user specified command line options exist?
  #-------------------------------------------------------------------
  argc = len( sys.argv )
  if argc != 2 :
    Usage()
  else :
    #-----------------------------------------------------------------
    # Save the "Current Working Directory"
    #-----------------------------------------------------------------
    here = os.getcwd()
    try :
      #---------------------------------------------------------------
      # Retreive the fully qualified path to script that is running...
      #---------------------------------------------------------------
      pgm  = sys.argv[ 0 ]
      if not pgm.endswith( '.py' ) :
        raise ValueError, 'Script error: "%s"' % pgm
      tempfile = pgm[ :-2 ] + '$$$'
#     print 'tempfile: "%s"' % tempfile

      #---------------------------------------------------------------
      # User specified "WAS Home" directory
      #---------------------------------------------------------------
      washome = sys.argv[ 1 ]
      WASerror = '"%s" does not appear to be a WAS Home directory.' % washome

      #---------------------------------------------------------------
      # - Try to "cd" to washome
      # - Verify that "profiles" exists therein
      # - "cd" to profiles
      # - Get a list of the available profileNames
      # - For each profile, execute "serverStatus -all"
      # - Parse the result, looking for specific message identifiers
      #---------------------------------------------------------------
      os.chdir( washome )        # Attempt to "cd" to specified dir
      files = os.listdir( '.' )  # What files & directories exist here?
      if 'profiles' in files :
        try :
          os.chdir( 'profiles' )
          profiles = os.listdir( '.' )
#         print 'profiles: ' + ' '.join( profiles )
#         if os.path.isfile( tempfile ) : os.unlink( tempfile )
          for profile in profiles :
#           print 'profile: ' + profile,
            print profile,
            os.chdir( profile + os.sep + 'bin' )
            os.system( 'serverStatus.bat -all >' + tempfile )

            f = open( tempfile )
            text = f.read()
            f.close()

            status = text.splitlines()
#           print '\n' + text
            print
            for line in status :
              if line.startswith( 'ADMU0509I' ) :
                server = re.compile( '"(\w+)"' ).search( line )
                if server :
                  print '  stopped: ' + server.group( 1 )
              elif line.startswith( 'ADMU0508I' ) :
                server = re.compile( '"(\w+)"' ).search( line )
                if server :
                  print '  running: ' + server.group( 1 )

            if os.path.isfile( tempfile ) : os.unlink( tempfile )

            os.chdir( '..' + os.sep + '..' )

        except :
          ( kind, info ) = sys.exc_info()[ :2 ]
          ( kind, info ) = str( kind ), str( info )
          print info
#         raise ValueError, WASerror

      else :
        raise ValueError, WASerror

    except :
      ( kind, info ) = sys.exc_info()[ :2 ]
      ( kind, info ) = str( kind ), str( info )
      print info

    #-----------------------------------------------------------------
    # Restore the Saved Working Directory
    #-----------------------------------------------------------------
    os.chdir( here )


#---------------------------------------------------------------------
# Name: Usage()
# Role: Descript script function
#---------------------------------------------------------------------
def Usage( cmdName = 'WSASstatus' ) :
  text = [ 'Program: %(cmdName)s\n',
           '   Role: Locate Application Server profile entries, and',
           '         determine the current status of each AppServer.\n',
           '  Usage: python WSASstatus.py <WAS_HOME>\n',
           'Example: python WSASstatus.py C:\\IBM\WebSphere\\AppServer' ]
  message = '\n'.join( text )
  print message % locals()
  sys.exit( -1 )

#---------------------------------------------------------------------
# main entry point - verify that script was executed, not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  WSASstatus()
else :
  Usage( __name__ )