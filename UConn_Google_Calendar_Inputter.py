from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datefinder
import datetime
from datetime import timedelta, timezone
import Txt_To_Calendar_Input



scopes = ['https://www.googleapis.com/auth/calendar']

#Prompts the user to authorize the application
flow = InstalledAppFlow.from_client_secrets_file("client_secret_.json", scopes=scopes)
credentials = flow.run_console()

#Stores the credentials
pickle.dump(credentials, open("token.pkl", "wb")) 
credentials = pickle.load(open("token.pkl", "rb"))

service = build("calendar", "v3", credentials=credentials)

result = service.calendarList().list().execute()

#Accesses the primary calendar
calendar_id = result['items'][0]['id']

#Displays all events in the primary calendar
result = service.events().list(calendarId=calendar_id).execute()

#Creates an event in the calendar
def create_event(summary, description, start_time, end_time, location=None, repeatWeeklyUntil=None):
    
    #Extracts the start and end times from text
    matches = list(datefinder.find_dates(start_time))
    matches2 = list(datefinder.find_dates(start_time))

    start_time = matches[0]
    end_time = matches2[0]

    #Converts the start and end time to a format accepted by the Google Calendar API
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    if repeatWeeklyUntil is not None:
      matches = list(datefinder.find_dates(repeatWeeklyUntil))
      repeatWeeklyUntil = matches[0]
      repeatWeeklyUntil = repeatWeeklyUntil.strftime("RRULE:FREQ=WEEKLY;UNTIL=%Y%m%d")

    #Creates the event
    event = {
      'summary': summary,
      'location': location,
      'description': description,
      'start' : {
          'dateTime': start_time,
          'timeZone': 'EST'
      },

      'end': {
        'dateTime': end_time,
        'timeZone': 'EST'
      },
      'recurrence': [
        repeatWeeklyUntil,
      ],
      'reminders': {
        'useDefault': False,
      }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

#Converts user input to output that can be read an turned into events in the calendar
Txt_To_Calendar_Input.run()

#Creates an event in the users google calendar for each class in the output file
classes = open("OutputFile.txt", "r")
for line in classes.readlines():
  classList = line.split(",")
  create_event(classList[0],  #Summary
              classList[1],   #Description
              classList[2],   #Start time
              classList[3],   #End time
              classList[4],   #Location
              classList[5])   #Repeat weekly until