---ZenDesk Integration for mon360---

Note: Eventually this may all be moved into the IncidentManagement ZenPack but for now this works


Purpose: Automate creation of ZenDesk ticket to inform customers that a collector host has gone offline


Requirements: https://github.com/zenoss/zenoss-RM-api


Setup: 

Download the RM API bundle and place it on the DFS at:

/opt/serviced/var/volumes/{volume_id}/var-zenpacks/zenoss-RM-api-master/

Add collectorHostDown.py, collectorHostUp.py and setProductionState.py to the directory above

Create an CZ API user and key on mon360 and configure creds.cfg file in zenoss-RM-api-master per rmApi documentation

Create a ZenDesk user with an API key to populate in collectorHostDown.py and collectorHostUp.py files

In mon360 create a command notification that paths appropriately to the scripts, examples:

-------------------------------------------------------------
	Command:
		/var/zenoss/zenoss-RM-api-master/collectorHostDown.py -c ${evt/device} -e ${dev/cEmergencyContact} -C ${dev/cEmergencyContactCCList} -E ${evt/evid} && /var/zenoss/zenoss-RM-api-master/setProductionState.py ${evt/device} 300

	Clear Command:
		/var/zenoss/zenoss-RM-api-master/collectorHostUp.py -c ${evt/device} -e ${dev/cEmergencyContact} -E ${evt/evid} -n ${evt/zenoss.IncidentManagement.number} && /var/zenoss/zenoss-RM-api-master/setProductionState.py ${evt/device} 1000

-------------------------------------------------------------

Add cEmergencyContact and cEmergencyContactCCList to mon360 and populate it with an email(s):
	
	cEmergencyContact must be a valid ZenDesk user this is the user the ZenDesk ticket will be opened under
        cEmergencyContactCCList can be as many emails as needed, however for this to work the must be on a single line with exactly one blank space between emails ie:
        	"person1@customer.com person2@customer.com person3@customer.com"

Add the appropriate collector host down detecting trigger to the notification



Validate:


To Do: 

Adjust messaging in the host down script, provide actions to perform, next steps, etc

