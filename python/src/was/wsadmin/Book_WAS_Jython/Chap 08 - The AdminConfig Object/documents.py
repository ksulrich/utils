#-------------------------------------------------------------------------------
# Name: documents.py
# From: WebSphere Application Server Administration using Jython
#   By: Robert A. (Bob) Gibson [rag], Arthur Kevin McGrath, Noel J. Bergman
# ISBN: 0-13-700952-6
# Role: Demonstrate AdminConfig document related methods
# History:
#   date   ver who what
# -------- --- --- ------------------------------------------
# 09/10/29 0.1 rag Fix - Added ISBN detail
# 08/10/21 0.0 rag New - for the book
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name: documents()
# Role: Extract the name of the file in the user supplied file specifier
#       Use this file to perform the call the following AdminConfig methods
#       - checkin()
#       - createDocument()
#       - deleteDocument()
#       - existsDocument()
#       - extract()
#-------------------------------------------------------------------------------
def documents( fileSpec ) :
  import re, os, tempfile
# print 'fileSpec: "%s"' % fileSpec
  #-----------------------------------------------------------------------------
  # Use a RegExp to locate the filename portion of the file specifier
  #-----------------------------------------------------------------------------
  fnPat = re.compile( '([^:\\\/]+)$' ).search( fileSpec )
  if fnPat :
    filename = fnPat.group( 1 )
#   print 'filename: "%s"' % filename
    #---------------------------------------------------------------------------
    # Verify that the user specified file exists
    #---------------------------------------------------------------------------
    if os.path.exists( fileSpec ) :
      node = AdminConfig.list( 'Node' ).splitlines()[ -1 ]
      print 'node: %s' % node
      uri  = node[ node.find( '(' ) + 1 : node.find( '|' ) ] + '/' + filename
      print '       documentURI: %s' % uri
      if AdminConfig.existsDocument( uri ) :
        AdminConfig.deleteDocument( uri )
        print '  Document removed.'
      else :
        cDigest = AdminConfig.createDocument( uri, fileSpec )
        print '  Document created.'
        tempName = tempfile.mktemp()
        print '    Temporary file: %s' % tempName
        eDigest  = AdminConfig.extract( uri, tempName )
        print 'Document extracted.  digest: %s' % eDigest
        AdminConfig.checkin( uri, tempName, eDigest )
        print 'Document checkedin'
        AdminConfig.deleteDocument( uri )
        print '  Document removed.'
    else :
      print 'File not found: %s\n' % fileSpec
      Usage()
  else :
    print 'Invalid file specifier: %s\n' % fileSpec
    Usage()

#-------------------------------------------------------------------------------
# Name: Usage()
#-------------------------------------------------------------------------------
def Usage( cmd = 'documents' ) :
  print '''     File: %(cmd)s.py\n
     Role: Script used to demonstrate some use for the AdminConfig "document"
           related methods.\n
     From: WebSphere Application Server Administration using Jython
   Author: Robert A. (Bob) Gibson
Published: July 2009 - IBM Press
     ISBN: <TBD>\n
Usage:
  wsadmin -conntype none %(cmd)s.py filename\n
Example:
  wsadmin -conntype none %(cmd)s.py c:\\bob.txt''' % locals()

#-------------------------------------------------------------------------------
# Role: main entry point
# Note: The use of repr() around sys.argv[ 0 ] is used to allow this script to
#       be run on Windows machines where '\\' is used as a directory delimiter.
#-------------------------------------------------------------------------------
argc = len( sys.argv )
if ( __name__ == 'main' ) or ( __name__ == '__main__' ) :
  if ( argc == 1 ) :
    documents( repr( sys.argv[ 0 ] )[ 1:-1 ] )
  else :
    Usage()
else :
  Usage( __name__ )
