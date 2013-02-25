#---------------------------------------------------------------------
#  Name: AttributeHelp.py
#  From: WebSphere Application Server Administration using Jython
#    By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
#  ISBN: 0-13-700952-6
#  Role: Generate the list of attributes for each configuration type
#        recognized by the WebSphere Application Server
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.2 rag Fix - Added ISBN detail
# 08/10/23 0.1 rag Minor cleanup for book
# 08/05/03 0.0 rag New - Based upon work for book
#---------------------------------------------------------------------

#---------------------------------------------------------------------
# Name: AttributeHelp()
# Role: Generate the list of attributes for each configuration type
#---------------------------------------------------------------------
def AttributeHelp() :
  dashes = '\n#' + '-' * 79;
  types = AdminConfig.types().splitlines();
  for typeName in types :
    helpText = AdminConfig.attributes( typeName ).splitlines();
    print '%(dashes)s\n# AdminConfig.attributes( "%(typeName)s" )%(dashes)s' % locals();
    for data in helpText :
      ( attr, text ) = data.split( ' ', 1 );
      if len( attr ) < 8 :
        delim = '';
      else :
        delim = '\n';
      if len( text ) < 72 :
        delim += '\t';

      if len( text ) > 72 :
        ( info, text ) = ( text, '' );
        while len( info ) > 72 :
          pos = info.rfind( ' ', 0, 73 );
          text += '\n\t' + info[ 0 : pos ];
          info = info[ ( pos + 1 ) : ];
        text += '\n\t' + info
      else :
        text = ' ' + text;
      print '%s%s%s' % ( attr, delim, text[ 1: ] );

#-------------------------------------------------------------------------------
# Name: Usage()
#-------------------------------------------------------------------------------
def Usage( cmd = 'AttributeHelp' ) :
  print '''     File: %(cmd)s.py\n
     Role: Generate the list of attributes for each configuration type
           recognized by the WebSphere Application Server.\n
     From: WebSphere Application Server Administration using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:
  wsadmin [-conntype none] -lang jython -f %(cmd)s.py\n
Example:
  wsadmin -conntype none -lang jython -f %(cmd)s.py >%(cms)s.out''' % locals()

#---------------------------------------------------------------------
# Role: main entry point
# main: Verify that this file was executed, and not imported
#---------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  AttributeHelp()
else :
  Usage( __name__ )
