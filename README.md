# UConn Google Calendar Scheduler
A Python Application that uploads your UConn Schedule to your Google Calendar
## How to use
1. Download the repository
2. Go to the [Google Developer Console](https://console.developers.google.com/)
3. Create a new project 
4. Enable the Google Calendar API
5. Go to credentials
6. Create credentials-OAuth client ID-Other
7. Download the Client ID and save as client_secret.json
8. Replace the client_secret.json file in the folder containing UConn_Google_Calendar_Inputter.py
9. Copy and paste your from schedule from the [UConn Self Service](https://studentadmin.uconn.edu/) site into InputFile.txt 
![Image of Schedule](/ScheduleImage.png)
10. Run UConn_Google_Calendar_Inputter.py
11. Go to the generated link
12. Select and verify which gmail account you would like to use
13. Paste the verification code into the console and press enter
14. Your UConn schedule should now be in your google calendar
