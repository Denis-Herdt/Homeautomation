import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import time
import datetime
while 1:
	try:
	    import argparse
	    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	except ImportError:
	    flags = None

	SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Google Calendar API Quickstart'


	def get_credentials():
	    """Gets valid user credentials from storage.

	    If nothing has been stored, or if the stored credentials are invalid,
	    the OAuth2 flow is completed to obtain the new credentials.

	    Returns:
		Credentials, the obtained credential.
	    """
	    home_dir = os.path.expanduser('~')
	    credential_dir = os.path.join(home_dir, '.credentials')
	    if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	    credential_path = os.path.join(credential_dir,
			                   'calendar-quickstart.json')

	    store = oauth2client.file.Storage(credential_path)
	    credentials = store.get()
	    if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
		    credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatability with Python 2.6
		    credentials = tools.run(flow, store)
		print 'Storing credentials to ' + credential_path
	    return credentials

	def main():
	    """Shows basic usage of the Google Calendar API.

	    Creates a Google Calendar API service object and outputs a list of the next
	    10 events on the user's calendar.
	    """
	    credentials = get_credentials()
	    http = credentials.authorize(httplib2.Http())
	    service = discovery.build('calendar', 'v3', http=http)

	    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	    print 'Getting the upcoming 10 events'
	    eventsResult = service.events().list(
		calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
		orderBy='startTime').execute()
	    events = eventsResult.get('items', [])

	    if not events:
		print 'No upcoming events found.'
	    for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
	        print start, event['summary']
		end = event['end'].get('dateTime', event['end'].get('date'))
	
	
	
	################################################################################################################      
	############################################## Openhab-Controller ##############################################
	################################################################################################################

	#################### Set morning-/nighttime ##################
		#morning = datetime.datetime.today().time().replace(hour=6, minute=0,second=0, microsecond=0)
                nighttime1 = datetime.datetime.today().replace(hour=15, minute=21,second=0, microsecond=0)
                nighttime2 = datetime.datetime.today().replace(hour=15, minute=23,second=0, microsecond=0)
                night = (nighttime1 <= datetime.datetime.now() and nighttime2 >= datetime.datetime.now())
	#################### Set functions ##################
		def thermo_on():
			heat = "ON"
			os.system("curl --header 'Content-Type: text/plain' --request POST --data '24' http://localhost:8080/rest/items/Thermostat1_Set")
		   	os.system("curl --header 'Content-Type: text/plain' --request POST --data '24' http://localhost:8080/rest/items/Thermostat2_Set")
		    	os.system("curl --header 'Content-Type: text/plain' --request POST --data '24' http://localhost:8080/rest/items/Thermostat3_Set")
		def thermo_off():
			heat = "OFF"
			os.system("curl --header 'Content-Type: text/plain' --request POST --data '8' http://localhost:8080/rest/items/Thermostat1_Set")
		    	os.system("curl --header 'Content-Type: text/plain' --request POST --data '8' http://localhost:8080/rest/items/Thermostat2_Set")
		    	os.system("curl --header 'Content-Type: text/plain' --request POST --data '8' http://localhost:8080/rest/items/Thermostat3_Set")
		#Try to get location form event (not always available)
		try:
		    location = event["location"]
		except:
		    location = "undefined"
		
        #################### Event Start-Time ##################

                stime = event['start'].get('dateTime', event['start'].get('date'))[11:19]
                if(event['start'].get('dateTime') == None):
			stime = "00:00:00"
		syear = event['start'].get('dateTime', event['start'].get('date'))[0:4]
                smonth = event['start'].get('dateTime', event['start'].get('date'))[5:7]
                sday = event['start'].get('dateTime', event['start'].get('date'))[8:10]
                sdate = syear+"-"+smonth+"-"+sday #formated starttime
                scompl= datetime.datetime.strptime(str(sdate) +" "+ str(stime), "%Y-%m-%d %H:%M:%S")

        #################### Event End-Time ##################
                etime = event['end'].get('dateTime', event['end'].get('date'))[11:19]
                if(event['end'].get('dateTime') == None):
			etime = "23:59:59"
                eyear = event['end'].get('dateTime', event['end'].get('date'))[0:4]
                emonth = event['end'].get('dateTime', event['end'].get('date'))[5:7]
                eday = event['end'].get('dateTime', event['end'].get('date'))[8:10]
                edate = eyear+"-"+emonth+"-"+eday #formated end-date
                ecompl= datetime.datetime.strptime(str(edate) +" "+ str(etime), "%Y-%m-%d %H:%M:%S")

	######################## Define timescopes for start heating ########################	
		startscopes = [120,60,30,3] # time to start heating befor eventstart(in minutes)
		startscopenum = 0
		for i in range(0, len(startscopes)): #creates a timescope for 2 minutes. In this time the thermostats start heating
		    eventstart1 = scompl - datetime.timedelta(minutes=startscopes[i])
		    eventstart2 = scompl - datetime.timedelta(minutes=startscopes[i]-2)
		    starttime = (eventstart1 <= datetime.datetime.today() and eventstart2 >=datetime.datetime.today())

		    if starttime:
			startscopenum = i
			break
	
	######################## Define timescopes for stop heating ########################
		endscopes = [10] # time to stop heating befor eventend(in minutes)
		endscopenum = 0
		for i in range(0, len(endscopes)): #creates a timescope for 2 minutes. In this time the thermostats stop heating
		    eventend1 = ecompl - datetime.timedelta(minutes=endscopes[i])
		    eventend2 = ecompl - datetime.timedelta(minutes=endscopes[i]-2)
		    endtime = endtime= (eventend1 <= datetime.datetime.today() and eventend2 >=datetime.datetime.today() and not starttime)
		    
		    if endtime:
			endscopenum = i
			break
	
	######################## Define roomselection ########################
		room = ((location == "K003") or (location == "K003A") or (location == "K003a")or (location == "k003")or (location == "k003A")or (location == "k003a"))
	 	
	######################## Regulate heating specified by room and time ###################
		if room and starttime: # check room and start-timescopes
		    	heat = "ON"
		    	print "\n^^^^^^^^^^^^^^^ heating ON ^^^^^^^^^^^^^^"
		    	print event["summary"] ," starts in less than " , startscopes[startscopenum] , " min!"
	#	    	print "Event starts in less than " , startscopes[startscopenum] , " min!"
		    	print 'Current time: ', datetime.datetime.today()
		    	print 'Event start time: ', scompl
		    	print 'Event end time:   ', ecompl
		    	print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
		    	thermo_on()
			break    
		elif room and endtime: # check room, end-timescopes and morning/night
		    	heat = "OFF"
		    	print "\nvvvvvvvvvvvvvv heating OFF vvvvvvvvvvvvvv"
		    	print event["summary"] ," ends in  less than " , endscopes[endscopenum] , " min!"
	#	    	print "Event ends in  less than " , endscopes[endscopenum] , " min!"
		    	print 'Current time: ', datetime.datetime.today()
		    	print 'Event start time: ', scompl
		    	print 'Event end time   ', ecompl
		    	print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n"
		    	thermo_off()
		  	break
                elif (night):
                        print "\nvvvvvvvvvvvvvv heating OFF vvvvvvvvvvvvvv"
                        print 'It is ', datetime.datetime.now(), " o'clock. Stop heating!"
                        print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv\n"
                        thermo_off()
                        break

	######################### Print Event-Infos ########################
		#print "\n++++++++++++++++ Event-Infos ++++++++++++++++"
		#print "Title:           ", event['summary']
		#print "Location:        ", location
		#print "-------- Statistic --------"
		#print "Room:            ", room
		#print "starttime:       ", starttime
		#print "Endtime:         ", endtime
		#print "Heat:            ", heat
		#print "----------- Time ----------"
		#print "Eventstart:       ", scompl
		#print "Eventend:         ", ecompl
		#print "+++++++++++++++++++++++++++++++++++++++++++++"
	    
	  ######################### Print Time-Infos ########################
	    
		#print "\n++++++++++++++ Heating-Infos ++++++++++++++++"
		#print "---------- Start ----------"
		#print "Startscopes:     ", startscopes
		#print "any fitting:     ", starttime
		#print "----------- End -----------"
		#print "Endscopes:       ", endscopes
		#print "any fitting:     ", endtime
		#print "++++++++++++++ event finished +++++++++++++++"
		#print "+++++++++++++++++++++++++++++++++++++++++++++"

	if __name__ == '__main__':
	    main()
	time.sleep(30)
