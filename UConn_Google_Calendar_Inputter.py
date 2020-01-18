import apiclient
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datefinder
import datetime
from datetime import timedelta, timezone
import PySimpleGUI as sg

#Gets the user input using a GUI
#A dark blue theme similar to the UConn color scheme
sg.theme('DarkBlue13')

#The text and buttons inside the window
layout = [  [sg.Text('Paste your class schedule here'), sg.InputText()],
            [sg.Button('Enter'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('UConn Class Schedule Inputter', layout)

event, values = window.read()

#Opens a file to store user input
inputFile = open("InputFile.txt", "w")

#Writes the user input to the calendar
inputFile.write(values[0])
inputFile.close()

#Close the window
window.close()


scopes = ['https://www.googleapis.com/auth/calendar']

#Prompts the user to authorize the application
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
credentials = flow.run_local_server(port=0)

#Stores the credentials
pickle.dump(credentials, open("token.pkl", "wb")) 
credentials = pickle.load(open("token.pkl", "rb"))

service = apiclient.discovery.build("calendar", "v3", credentials=credentials)

#Creates an event in the calendar
def create_event(summary, description, start_time, end_time, location=None, repeatWeeklyUntil=None):
    
    #Extracts the start and end times from text
    matches = list(datefinder.find_dates(start_time))
    matches2 = list(datefinder.find_dates(end_time))

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

def run():
    #Opens the user input file
    fileInput = open("InputFile.txt", "r")

    #Creates a list to store information about each class
    classInfo = []

    #A variable that keeps track of the first time through the loop
    first = True

    #Finds the date of the next weekday
    #0 = monday, 1 = tuesday, etc
    def nextWeekday(day, weekday):
        days_ahead = weekday - day.weekday()
        if days_ahead < 0:
            days_ahead += 7
        return day + datetime.timedelta(days_ahead)


    #Operates on every line of the file and if the line contains class info appends it to the list
    for line in fileInput.readlines():
        if "Spring" in line:
            if "2020" in line:
                startDate = datetime.date(2020, 1, 21)
                stopDate = "5/1/2020"
            elif "2021" in line:
                startDate = datetime.date(2021, 1, 19)
                stopDate = "4/30/2021"
            elif "2022" in line:
                startDate = datetime.date(2022, 1, 18)
                stopDate = "4/29/2022"
            elif "2023" in line:
                startDate = datetime.date(2023, 1, 17)
                stopDate = "4/28/2023"
        if "Fall" in line:
            if "2020" in line:
                startDate = datetime.date(2020, 8, 31)
                stopDate = "12/11/2020"
            elif "2021" in line:
                startDate = datetime.date(2021, 8, 30)
                stopDate = "12/11/2021"
            elif "2022" in line:
                startDate = datetime.date(2022, 8, 29)
                stopDate = "12/9/2022"

        if "Schedule" not in line:
            
            if "Academic Calendar Deadlines" in line:
                #The first time through no class info has been read yet
                if first:
                    first = False
                else:
                    #Shows an end to information for a class
                    classInfo.append("|")

            else:
                #Adds the class info to the list
                classInfo.append(line)

    fileInput.close()

    #Shows an end to information for the last class
    classInfo.append("|")

    #Converts the class info into a list of lists where each sublist contains the information for a class
    def classInfoList(classInfo):
        listOfClassInfo = []
        
        listAcc = []

        for info in classInfo:
            if "|" in info:
                listOfClassInfo.append(listAcc)
                listAcc = []
            else:
                listAcc.append(info)
            
        return listOfClassInfo


    #Returns a list of dates with start time and end time
    def dayTimeConverter(dayTime):

        days = []
        split = dayTime.split()
        times = [split[1], split[3]]

        if "Mo" in dayTime:
            days.append([nextWeekday(startDate, 0), times]) #Finds the first monday of the semester
        if "Tu" in dayTime:
            days.append([nextWeekday(startDate, 1), times]) #Finds the first tuesday of the semester
        if "We" in dayTime:
            days.append([nextWeekday(startDate, 2), times]) #etc
        if "Th" in dayTime:
            days.append([nextWeekday(startDate, 3), times])
        if "Fr" in dayTime:
            days.append([nextWeekday(startDate, 4), times])
        if "Sa" in dayTime:
            days.append([nextWeekday(startDate, 5), times])
        if "Su" in dayTime:
            days.append([nextWeekday(startDate, 6), times])

        return days



    #Opens the output file
    output = open("OutputFile.txt", "w")

    #Writes the class to the file
    def addClass(information):

        #More than 1 time/location
        if len(information) > 4:
            information[2] = dayTimeConverter(information[2])
            for days in information[2]:
                output.write("%s, %s, %s %s, %s %s, %s, %s" % (information[0].rstrip("\n"), #Class name/number
                                                                information[1].rstrip("\n"), #Description ie: lec, lab
                                                                days[0], days[1][0], #Date and start time
                                                                days[0], days[1][1], #Date and end time
                                                                information[3].rstrip("\n"), #Location
                                                                stopDate)) #Last day of the semester
                output.write("\n")

            information[4] = dayTimeConverter(information[4])
            for days in information[4]:
                output.write("%s, %s, %s %s, %s %s, %s, %s" % (information[0].rstrip("\n"), #Class name/number
                                                                information[1].rstrip("\n"), #Description ie: lec, lab
                                                                days[0], days[1][0], #Date and start time
                                                                days[0], days[1][1], #Date and end time
                                                                information[5].rstrip("\n"), #Location
                                                                stopDate)) #Last day of the semester
                output.write("\n")

        #One time/location
        elif len(information) > 3:
            information[2] = dayTimeConverter(information[2])
            for days in information[2]:
                output.write("%s, %s, %s %s, %s %s, %s, %s" % (information[0].rstrip("\n"), #Class name/number
                                                                information[1].rstrip("\n"), #Description ie: lec, lab
                                                                days[0], days[1][0], #Date and start time
                                                                days[0], days[1][1], #Date and end time
                                                                information[3].rstrip("\n"), #Location
                                                                stopDate)) #Last day of the semester
                output.write("\n")
            
            

    classInfo = classInfoList(classInfo)
    for info in classInfo:
        addClass(info)

    output.close()

#Converts user input to output that can be read an turned into events in the calendar
run()

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

classes.close()
