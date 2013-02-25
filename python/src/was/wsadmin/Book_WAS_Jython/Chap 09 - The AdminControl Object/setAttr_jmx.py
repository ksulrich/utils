#---------------------------------------------------------------------
# Name: setAttr_jmx.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Use command line arguments to set TraceSpecification value
#       via the AdminControl.setAttributes_jmx() method
# Note: See Usage() for more details.
#---------------------------------------------------------------------
# History:
#   date   ver who what
# -------- --- --- ----------------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/11/12 0.0 rag New - for the book
#---------------------------------------------------------------------
import getopt, sys

#---------------------------------------------------------------------
# Global dictionary to hold the user specified options & values
#---------------------------------------------------------------------
Opts = {}

#---------------------------------------------------------------------
# Name: validWord
# Role: Verify that the specified name, contains at least 1 char, and
#       only uses "word" characters (i.e., [a-zA-Z0-9_]
#---------------------------------------------------------------------
def validWord( name ):
  import re
  return ( re.search( re.compile( r'^\w+$' ), name ) != None )

#---------------------------------------------------------------------
# Name: setAttr_jmx()
# Role: Use command line arguments to set TraceSpecification value
#       via the AdminControl.setAttributes_jmx() method
#---------------------------------------------------------------------
def setAttr_jmx( cmdName = 'setAttr_jmx' ) :
  #-------------------------------------------------------------------
  # Check for command line parameters
  #-------------------------------------------------------------------
  argc = len( sys.argv )                    # Number of arguments
  parseOpts( cmdName )                      #   parse the command line

  #-------------------------------------------------------------------
  # Assign values from the user Options dictionary.  To make value
  # access simplier.  For example, instead of using:
  #   Opts[ 'servName' ]
  # we will be able to simply use:
  #   servName
  # to access the value.  In addition, we can make use of these names
  # in any mapped messages, see unknownNode below.
  #-------------------------------------------------------------------
  for key in Opts.keys() :
    cmd = str( key ) + ' = Opts[ "' + str( key ) + '" ]'
    exec( cmd )

  try :
    #-----------------------------------------------------------------
    # import the required modules
    #-----------------------------------------------------------------
    import javax.management as mgmt
    from WAuJ_utilities import MBattrAsDict

    #-------------------------------------------------------------------
    # Check that servName, if provided, is valid (alphanumeric)
    #-------------------------------------------------------------------
    if servName and not validWord( servName ) :
      print 'Invalid serverName value: ' + str( servName )
      Usage( cmdName )

    #-------------------------------------------------------------------
    # Check that nodeName, if provided, is valid (alphanumeric)
    #-------------------------------------------------------------------
    if nodeName and not validWord( nodeName ) :
      print 'Invalid nodeName value: ' + str( nodeName )
      Usage( cmdName )

    #-----------------------------------------------------------------
    # Get the MBean name string for a unique TraceService object instance
    #-----------------------------------------------------------------
    query = 'type=TraceService,*'
    if nodeName :
      query = 'node=%s,%s' % ( nodeName, query )
    if servName :
      query = 'process=%s,%s' % ( servName, query )

#   print 'query: ' + query
    ts = AdminControl.queryNames( query ).splitlines()
#   print 'len( ts ) = %d' % len( ts )

    #-----------------------------------------------------------------
    # Was a unique, and available TraceService indicated?
    #-----------------------------------------------------------------
    if len( ts ) < 1 :
      print '%(cmdName)s: error - specified server not available' % locals()
      sys.exit( 1 )

    if len( ts ) > 1 :
      print '%(cmdName)s: ambiguous request - a unique server must be indicated' % locals()
      sys.exit( 1 )

    #-----------------------------------------------------------------
    # Convert the MBean name string to an MBean name
    #-----------------------------------------------------------------
    tsName = AdminControl.makeObjectName( ts[ 0 ] )
#   print 'tsName: ' + str( tsName )

    #-----------------------------------------------------------------
    # Put the MBean attributes information into a dictionary
    #-----------------------------------------------------------------
    tsDict = MBattrAsDict( ts[ 0 ] )
#   print 'keys(): ' + str( tsDict.keys() )

    #-----------------------------------------------------------------
    # Locate the "modifiable" attributes
    # width == The length of the longest modifiable attribute name
    #-----------------------------------------------------------------
    names  = tsDict[ 'Modifiable' ]
    width  = max( [ len( x ) for x in names ] )
#   print 'names: ' + str( names )

    #-----------------------------------------------------------------
    # Example use of getAttributes_jmx() to obtain the current value
    # of a specific set of attributes of a given object.
    # Note: The MBean name identifies the object instance in question
    #-----------------------------------------------------------------
    print '%s : modifiable attributes - current values\n%s' % ( cmdName, '-' * 70 )
    attr = AdminControl.getAttributes_jmx( tsName, names )
    for att in attr :
      print '%*s : %s' % ( width, att.getName(), att.getValue() )
    print '-' * 70 + '\n'

    #-----------------------------------------------------------------
    # The setAttributes_jmx() routine requires the 2nd parameter to be
    # of type AttributeList.
    #-----------------------------------------------------------------
    if traceSpec :
#     print '\ntraceSpec to be used: ' + traceSpec
      aList = mgmt.AttributeList()
      aList.add( mgmt.Attribute( 'traceSpecification', traceSpec  ) )

      #---------------------------------------------------------------
      # Invoke setAttributes_jmx() to try and modify some attributes
      #---------------------------------------------------------------
      print 'setAttributes_jmx() result:\n%s' % ( '-' * 70 )
      for att in AdminControl.setAttributes_jmx( tsName, aList ) :
        print '%*s : %s' % ( width, att.getName(), att.getValue() )
      print '-' * 70

  except SystemExit, rc :
    sys.exit( rc )
  except ImportError, ie :
    modName = str( ie ).split( ' ' )[ -1 ]
    print '%(cmdName)s: Error - Required module not found: %(modName)s' % locals()
    sys.exit( 1 )
  except :
    ( kind, info ) = sys.exc_info()[ :2 ]
    ( kind, info ) = str( kind ), str( info )
    seTxt = 'ScriptingException'              # Special exception text
    sePos = info.find( seTxt )
    if sePos > -1 :
      seMsg = info[ sePos + len( seTxt ) + 2 : ]
      if seMsg.startswith( 'AdminControl' ) :
        print '%s: error - An Application Server connection is required.' % cmdName
      else :
        print '%s: error - %s' % ( cmdName, seMsg )
    else :
      print '''%(cmdName)s: unexpected error encountered.
  Exception type: %(kind)s
  Exception info: %(info)s''' % locals()

#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  #-------------------------------------------------------------------
  # Short (sOpts) & Long (lOpts) form option flags, and
  # mapped error messages
  #-------------------------------------------------------------------
  sOpts = 'n:s:t:'
  lOpts = 'nodeName=,serverName=,traceSpec='.split( ',' )
  badOpt = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s'
  optErr = '%(cmdName)s: Error encountered processing: %(argStr)s'

  #-------------------------------------------------------------------
  # Use the previously defined short and long form option values to
  # parse/process the user specified command line options.
  # Note: Should an unknown option be encountered, a GetoptError will
  #       be raised.
  #-------------------------------------------------------------------
  try :
    opts, args = getopt.getopt( sys.argv, sOpts, lOpts )
  except getopt.GetoptError:
    argStr = ' '.join( sys.argv )
    print optErr % locals()
    Usage( cmdName )                # print help information and exit

  #-------------------------------------------------------------------
  # Initialize the global Opts dictionary using the following keywords
  #-------------------------------------------------------------------
  keys = 'servName,nodeName,traceSpec'.split( ',' )
  for key in keys : Opts[ key ] = None

  #-------------------------------------------------------------------
  # process the list of options returned by getOpt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in   ( '-s', '--serverName' ) : Opts[ 'servName'  ] = val
    elif opt in ( '-t', '--traceSpec'  ) : Opts[ 'traceSpec' ] = val
    elif opt in ( '-n', '--nodeName'   ) : Opts[ 'nodeName'  ] = val

  #-------------------------------------------------------------------
  # Check for unhandled/unrecognized options
  #-------------------------------------------------------------------
  if ( args != [] ) :
    argStr = ' '.join( args )
    if len( args ) > 1 :
      plural = 's'
    else :
      plural = ''
    print badOpt % locals()
    Usage( cmdName )

#---------------------------------------------------------------------
# Name: Usage()
#---------------------------------------------------------------------
def Usage( cmd = 'setAttr_jmx' ) :
  print '''Command: %(cmd)s.py\n
   From: WebSphere Application Server Administration using Jython
   ISBN: TBD\n
Purpose: Demonstrate the use of the AdminControl.setAttributes_jmx() method to
         view/modify the trace specification of the selected application server.\n
  Usage: %s [options]\n
Optional switches:
  -s | --serverName  <name>  = Name of server
  -n | --nodeName    <name>  = Name of node on which server exists
  -t | --traceSpec   <value> = traceSpecification to used.\n
Notes:
- Long form option values may be separated/delimited from their associated
  value using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated value using
  an optional space.\n
- Description text containing blanks should be enclosed in double quotes.\n
Examples:
  wsadmin -lang jython -f %s.py --serverName=s1 --traceSpec "*=info"\n
  wsadmin -lang jython -f %s.py -sserver1 -t"*=info:com.ibm.ws.*=all"''' % locals()
  sys.exit( 1 )

#--------------------------------------------------------------------
# main: Verify that script was executed, and not imported
#--------------------------------------------------------------------
if ( __name__ == 'main' ) or ( __name_ == '__main__' ) :
  setAttr_jmx()
else :
  Usage( __cmd__ )
