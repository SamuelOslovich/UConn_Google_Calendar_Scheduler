def run():
    #Opens the user input file
    fileInput = open("InputFile.txt", "r")

    #Creates a list to store information about each class
    classInfo = []

    #A variable that keeps track of the first time through the loop
    first = True

    #Operates on every line of the file and if the line contains class info appends it to the list
    for line in fileInput.readlines():
        
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
            days.append(["1/27/2020", times]) #1/27 is the first monday of the semester
        if "Tu" in dayTime:
            days.append(["1/21/2020", times]) #1/21 is the first tuesday of the semester
        if "We" in dayTime:
            days.append(["1/22/2020", times]) #etc
        if "Th" in dayTime:
            days.append(["1/23/2020", times])
        if "Fr" in dayTime:
            days.append(["1/24/2020", times])
        if "Sa" in dayTime:
            days.append(["1/25/2020", times])
        if "Su" in dayTime:
            days.append(["1/26/2020", times])

        return days

    #print(classInfoList(classInfo))



    #Opens the output file
    output = open("OutputFile.txt", "w")

    #Writes the class to the file
    def addClass(information):
        lastDayOfSemester = "5/1/2020"

        #More than 1 time/location
        if len(information) > 4:
            information[2] = dayTimeConverter(information[2])
            for days in information[2]:
                output.write("%s, %s, %s %s, %s %s, %s, %s" % (information[0].rstrip("\n"), #Class name/number
                                                                information[1].rstrip("\n"), #Description ie: lec, lab
                                                                days[0], days[1][0], #Date and start time
                                                                days[0], days[1][1], #Date and end time
                                                                information[3].rstrip("\n"), #Location
                                                                lastDayOfSemester)) #Last day of the semester
                output.write("\n")

            information[4] = dayTimeConverter(information[4])
            for days in information[4]:
                output.write("%s, %s, %s %s, %s %s, %s, %s" % (information[0].rstrip("\n"), #Class name/number
                                                                information[1].rstrip("\n"), #Description ie: lec, lab
                                                                days[0], days[1][0], #Date and start time
                                                                days[0], days[1][1], #Date and end time
                                                                information[5].rstrip("\n"), #Location
                                                                lastDayOfSemester)) #Last day of the semester
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
                                                                lastDayOfSemester)) #Last day of the semester
                output.write("\n")
            
            

    classInfo = classInfoList(classInfo)
    for info in classInfo:
        addClass(info)

    output.close