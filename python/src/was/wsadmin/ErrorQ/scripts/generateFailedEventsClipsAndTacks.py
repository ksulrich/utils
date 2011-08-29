#!/usr/bin/env python
#
# This script generates the input xml file for the BatchWriter tool
# to generate failed events for the ClipsAndTacks example

import sys

event = """
      <CommonBaseEvent msg=\"cbe3\" creationTime=\"2005-09-15T01:54:49.823Z\" extensionName=\"ActivityEvent\" 
        globalInstanceId=\"CE01DA258BB3569A10EC7FF61EB66D3990\" sequenceNumber=\"1\" 
        severity=\"10\" version=\"1.0.1\">

        <extendedDataElements name=\"ActivityEventData\" type=\"noValue\">
		<children name=\"businessUnit\" type=\"string\">
                <values>Clips And Tacks</values>
            </children>
		<children name=\"processName\" type=\"string\">
                <values>Order Handling</values>
            </children>
            <children name=\"activityName\" type=\"string\">
                <values>Check Customer Account Status</values>
            </children>
            <children name=\"eventType\" type=\"string\">
                <values>started</values>
            </children>
            <children name=\"activityState\" type=\"string\">
                <values>running</values>
            </children>
            <children name=\"startTime\" type=\"dateTime\">
                <values>2006-08-07T08:20:05Z</values>
            </children>
            <children name=\"endTime\" type=\"dateTime\">
                <values>2006-08-07T08:20:05Z</values>
            </children>
        </extendedDataElements>

        <extendedDataElements name=\"OrderBOData\" type=\"noValue\">
            <children name=\"orderNumber\" type=\"string\">
                <values>o1$ID$</values>
            </children>
            <children name=\"customerNumber\" type=\"string\">
                <values>cust0001</values>
         </children>
         <children name=\"orderState\" type=\"string\">
             <values>In Progress</values>
         </children>
         <children name=\"city\" type=\"string\">
             <values>Raleigh</values>
         </children>
         <children name=\"country\" type=\"string\">
             <values>USA</values>
         </children>
         <children name=\"productNumber\" type=\"string\">
             <values>sku1111</values>
         </children>
         <children name=\"quantity\" type=\"int\">
             <values>1</values>
         </children>
         <children name=\"totalPrice\" type=\"double\">
             <values>100.0</values>
         </children>
       </extendedDataElements>

	<sourceComponentId application=\"TestApplication\" component=\"TestComponent\" componentIdType=\"TestComponentIdType\" location=\"TestLocation\" locationType=\"IPV4\" subComponent=\"TestSubComponent\" componentType=\"TestComponentType\"/>	
	<situation categoryName=\"StartSituation\">
	        <situationType xsi:type=\"StartSituation\" reasoningScope=\"EXTERNAL\" successDisposition=\"SUCCESSFUL\" situationQualifier=\"START_COMPLETED\"/>                
	</situation>
    </CommonBaseEvent>
"""

if len(sys.argv) <= 1:
    print """
Usage: generateFailedEventsClipsAndTacks.pl <# of events>
       Generate <# of events> faile events to feed with the BatchWriter to to ClipsAndTacks
        """
    sys.exit(1)

counter = int(sys.argv[1])
print "<CommonBaseEvents>"

for i in range(0,counter):
    #print event.replace("$ID$", "xxx" + repr(i), 1)
    print event.replace("$ID$", "xxx", 1)

print "</CommonBaseEvents>"
