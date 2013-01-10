#---------------------------------------------------------------------
# Name: AdminConfigTypes.py
# Role: Generate the list of type names recognized by the WebSphere
#       AdminConfig scripting object.
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Note: Depends upon availability of WSAS Admin Objects
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.2 rag Fix - Added ISBN detail
# 08/10/17 0.1 rag Revised for book, including the addition of Usage()
# 08/02/29 0.0 rag New - Created for IMPACT 2008
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# Name: configTypes()
# Role: Generate the list of AdminConfig Types
#---------------------------------------------------------------------
def configTypes() :
  types = AdminConfig.types().splitlines();
  #-------------------------------------------------------------------
  # Use list comprehension to create a list containing the length
  # of each type name
  #-------------------------------------------------------------------
  lengths = [ len( x ) for x in types ]
  print '\n'.join( types )
  print '''
\n%d AdminConfig types listed.
Minimum item length: %d
Maximum item length: %d
''' % ( len( types ), min( lengths ), max( lengths ) );

#-------------------------------------------------------------------------------
# Name: Usage()
#-------------------------------------------------------------------------------
def Usage( cmd = 'AdminConfigTypes' ) :
  print '''     File: %(cmd)s.py\n
     Role: Script used to display the configuration types recognized by
           WebSphere Applicaiton Server.\n
     From: WebSphere Application Server Administration using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:
  wsadmin -conntype none -lang jython -f %(cms)s.py''' % locals()

#-------------------------------------------------------------------------------
# Role: main entry point - verify that script was executed & not imported
#-------------------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  try :
    configTypes();
  except :
    print 'WebSphere Application Server does not appear to be available.'
else :
  Usage( __name__ )