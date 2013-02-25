#
# database.py
#
# JDBC and DataSource scripts


def deleteVariablesWithNoValue():
  """Delete any variable that does not have a value"""
  vList = AdminConfig.list( 'VariableSubstitutionEntry' ).splitlines()
  print "Out of",str(  len(vList)  ),"WebSphere variables,"
  deleted = 0
  for v in vList:
    if len( AdminConfig.showAttribute( v, 'value' ) ) < 1:
      #print v
      #print AdminConfig.show( v )
      AdminConfig.remove( v )
      deleted = deleted + 1
  print str( deleted ), "were deleted"
  print "Type AdminConfig.save() if you wish to commit these changes"

def dumpAllVariables():
  """Show all variables at all scopes"""
  vList = AdminConfig.list( 'VariableSubstitutionEntry' ).splitlines()
  for v in vList:
    print v
    print AdminConfig.show( v )

def dumpPropertySet( setName, jaclList ):
  """Find a property and change its value
parameters:
  setName - String - the name of the propertySet
  jaclList - very long String - the complete value returned by AdminConfig.showAttribute() nested inside AdminConfig.show()"""
  delimeter = '`'
  # remove distractions
  jaclList = jaclList.replace( '[' + setName + ' [', '' )
  jaclList = jaclList.replace( ']]', '' )
  #create a reliable delimiter
  jaclList = jaclList.replace( ') ', ')' + delimeter )
  listOfProperties = jaclList.split( delimeter )
  print "There are",len(listOfProperties), "properties\n"
  for p in listOfProperties:
    print AdminConfig.showAttribute( p, 'name' ) \
          + "    " + AdminConfig.showAttribute( p, 'type' ) \
          + "    " + AdminConfig.showAttribute( p, 'value' )
    print AdminConfig.showAttribute( p, 'description' ) + '\n'


def changePropertySet( setName, jaclList, propertyName, propertyValue ):
  """Find a property and change its value
parameters:
   setName - String - the name of the propertySet
   jaclList - very long String - the complete value returned by AdminConfig.showAttribute() nested inside AdminConfig.show()
   propertyName - String - the name of the property we wish to change
   propertyValue - String - the new value.  '[]' means empty value
   You may NOT change the name of a property
   You must call AdminConfig.save() to make changes permanent"""
  delimeter = '`'
  # remove distractions
  jaclList = jaclList.replace( '[' + setName + ' [', '' )
  jaclList = jaclList.replace( ']]', '' )
  #create a reliable delimiter
  jaclList = jaclList.replace( ') ', ')' + delimeter )
  listOfProperties = jaclList.split( delimeter )
  for p in listOfProperties:
    if AdminConfig.showAttribute( p, 'name' ) == propertyName:
      if propertyValue == "[]":
        AdminConfig.modify( p, [[ 'value', [] ]] )
      else:
        AdminConfig.modify( p, [[ 'value', propertyValue ]] )
      print AdminConfig.queryChanges()
      break


def createDataSource():
  uid = "KevinsDataSource-User"
  pwd = "SuperToPSecret"
  desc = "This is an example of a JAAS Authentication Alias"
  DataBaseAccessAlias = "Boss/KevinsDatabaseCredentials"

  secMgrID = AdminConfig.list( 'Security' )

  jaasID = AdminConfig.create( 'JAASAuthData', secMgrID,  \
     [ ['alias', DataBaseAccessAlias],                  \
     ['description', desc],                             \
     ['userId', uid], ['password',pwd]  ] )

  p = AdminTask.createJDBCProvider('[-scope Node=Node01 -databaseType DB2 -providerType "DB2 Using IBM JCC Driver" -implementationType "XA data source" -name KevinsBrandNewProvider -description "This is a fairly simple thing to create" ]')

  d = AdminTask.createDatasource( p,      '[-name KevinsDataSource -jndiName jdbc/kevinsData -description "This DataSource pools connections from our JDBCProvider" -category "classroom exercise" -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -componentManagedAuthenticationAlias ' + DataBaseAccessAlias + ' -xaRecoveryAuthAlias ' + DataBaseAccessAlias + ' -configureResourceProperties [[databaseName java.lang.String KevinsToyClassroomDatabase] [serverName java.lang.String was7host01.ibm.com]]]')

