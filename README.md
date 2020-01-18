# UConn Google Calendar Scheduler
---
I came up the idea for this program when I was thinking about all the time that I spend inputting my college class schedule into my google calendar. I decided to make a program where I could copy and paste my schedule into an input field and my classes would automatically be uploaded to my google calendar. I decided to use python for this project since the google calendar api supports python and I had a class using python coming up. The user copies their class schedule from the UConn self service page and pastes it into the input field. The program saves the data inputted into the input field as a .txt file. The program then parses this new text file and converts it to a format where events can be created in the google calendar. I exported this program to an executable using pyinstaller. Currently the executable is windows only, and I have no plans to make a Linux or Mac executable in the forseeable future.
## How to use
1. Download the [executable](https://www.dropbox.com/s/zmjart8r48tq5go/UConn_Google_Calendar_Inputter.exe?dl=0)
2. Go to the [Google Developer Console](https://console.developers.google.com/)
3. Create a new project 
4. Enable the Google Calendar API
5. Go to credentials
6. Create credentials-OAuth client ID-Other
7. Download the Client ID and save as client_secret.json
8. Place the client_secret.json file in the folder containing UConn_Google_Calendar_Inputter.exe
9. Run UConn_Google_Calendar_Inputter.exe
10. Copy and paste your from schedule from the [UConn Self Service](https://studentadmin.uconn.edu/) site into the input field 
![Image of Schedule](ScheduleImage.PNG)
11. Select and verify which gmail account you would like to use
12. Your UConn schedule should now be in your google calendar
## Python Libraries Used
- pickle
- datefinder
- datetime
- google-api
- pysimplegui
