#Coursework B DADSA  
#Anthony Adams 16013428

#Goal of project is to create a decision support system for nurses to allow for speed acuracy and consistency 
#Overview of rules: Patients are classes by condition; High risk or low risk
#Patients are assessed by nurses every few hours and their feeding maybe adjusted based on data that is recorded
#Task 1 Design a suitable data strucutre(s) to employ and develop algorithm to support this decision making process -
#produce detailed pseudo code
#Task 2 A.Save new data per patient as it created in the cycle of evalutaion indicated in the flowchart. Utilise the new data together-
#with the data provided in each file to complete 5 day cycle of evaluation
#B. At the end of 24 hour period, print on screen an update showing each patients progress as they are fed and assessed through each-
#day over a period of 5 days
#C. At the end of the 5 day cycle, rank the list of patiens at the rate of improvement theyve shown and identify those who show lack-
#of progress - they need to be referred to dieticians and specialist clinicians. At te top of the list you should show the patients-
#that have been progressing their feeding regulalry. These should be followed by patients that have had their feeding by one or more-
#stopages. Finally at the bottom of the list you should show the patients that have had to be evaluated by dieticians as their feeding-
#had to be stopped for more than 8 hour.
#Task 3 A. Evaluate your design and implementation as to the effectiveness of the solution and the efficiency of the tools-
#(data structures and algorithms) employed
#B. Discuss the concept of security of the data used here and the legal concerns. WHat should the hospital be doing to secure the data-
#to be compliant with GDPR and other legislation in the UK

#Read in 10 csv files and create a new data structure that holds the information(No libraries can be used, even dicts, tuples etc)
#what is pn
#why does grv start at 3 not 4
#what determines rate of improvement a: not so much rate of improvement as whoever had none issues is first and whoever had the most is
#last

#Read file header record - store name, risk, age, weight
#skip blank record (',,,,')
#read or skip data header record ('DAY,TIME,FEED,GRV,ISSUES')
#LOOP TO read and store data record - day, time, feed, grv, issues
#skip trailing records (',,,,')
#=========================================================================================================

import csv
import os

class DataPoint:
    def __init__(self, day=None, time=None, feed=None, grv=None, issues=None):
        self.day = day
        self.time = time
        self.feed = feed
        self.grv = grv
        self.issues = issues

    def attrList(self):
        '''return the attributes of this data point as a list'''
        return [self.day, self.time, self.feed, self.grv, self.issues]

class Hospital:
    def __init__(self):
        self.patients = []

    def populatePatients(self):
        for root, dirs, files in os.walk("."):
            for csv_file in files:
                if "PATIENT DATA " in csv_file:
                    print (csv_file)
                    #with open(csv_file) as csvfile:
                    #    patList = csv.reader(csvfile)
                    #    for row in patList:
                    #        print(', '.join(row))
                    #        self.patients.append(Patient(row[0], row[2], row[4], row[1]))
                    self.patients.append(Patient(csv_file))

        
    def patientFeedingProcess(self):
        for p in self.patients:
            #Here is the cycle for patient feeding taken from the feeding guidelines
            print("...Analysing data for patient: {}".format(p.name))
            #print(p.name,p.age,p.weight)
            if p.risk == "HR":
                print("This Patient is High Risk")
                # Data points should have various feeding rates for the first 3 days which
                #  cover the first 72 hours + 4 hours = 76 hours for shifting to LOW RISK regime
                index = 75
            elif p.risk == "LR":
                print("This Patient is low risk")
                # Data points should have '5ML/2 HRS' (or '20ML/2 HRS' if weight > 40Kg)
                # recorded at datapoints[0] and datapoints[2] which cover the first 4 hours
                index = 4

            #check grv against critical value of 5MLs/KG
            critical_grv = 5 * p.weight
            secondary_grv = 250
            finished = False
            while not finished:
                if isinstance(p.datapoints[index].grv,str):
                    print("ERROR - no GRV whilst processing datapoint at index: {} day:{} time: {}" \
                            .format(index, int(index / 24) +1, p.datapoints[index].time))
                    print("ERROR - Datapoint values = day:{} time:{} feed:{} grv:{} issues:{}" \
                            .format(*p.datapoints[index].attrList()))
                    print("ERROR - Processing halted for patient '{}'".format(p.name))
                    p.datapoints[index].issues = "PROGRAM ANALYSIS HALTED - NO GRV VALUE FOUND"
                    break
                if p.datapoints[index].grv > critical_grv:
                    #If true replace all grv and pause feed for 2 hours then recheck grv
                    #Update feed to "FEED PAUSED" and issues to "FEEDING PAUSED"
                    p.datapoints[index].feed = "FEED PAUSED"
                    p.datapoints[index].issues = "FEEDING PAUSED"
                    index +=2
                    if isinstance(p.datapoints[index].grv,str):
                        print("ERROR - no GRV whilst processing datapoint at index: {} day:{} time: {}" \
                            .format(index, int(index / 24) +1, p.datapoints[index].time))
                        print("ERROR - Datapoint values = day:{} time:{} feed:{} grv:{} issues:{}" \
                            .format(*p.datapoints[index].attrList()))
                        print("ERROR - Processing halted for patient '{}'".format(p.name))
                        p.datapoints[index].issues = "PROGRAM ANALYSIS HALTED - NO GRV VALUE FOUND"
                        break
                    if (p.datapoints[index].grv > critical_grv and p.weight <= 40) \
                    or (p.datapoints[index].grv > secondary_grv and p.weight > 40):
                        #Refer to dietician
                        p.datapoints[index].issues = "REFER TO DIETICIAN"
                        finished = True
                    else:
                        #Replace GRV and increase feeds to 10ML/2hr (or 30ML/2hr if weight greater than 40kg)
                        if p.weight > 40:
                            p.datapoints[index].feed = "30ML /2 HRS" 
                        else:
                            p.datapoints[index].feed = "10ML /2 HRS"
                        p.datapoints[index].issues = "NONE"
                else:
                    #Replace GRV and increase feeds to 10ML/2hr (or 30ML/2hr if weight greater than 40kg)
                    if p.weight > 40:
                        p.datapoints[index].feed = "30ML /2 HRS" 
                    else:
                        p.datapoints[index].feed = "10ML /2 HRS"
                    p.datapoints[index].issues = "NONE"

                # next check in 4 hours time
                index +=4
                if index >= len(p.datapoints):
                    #No more data points to examine
                    finished = True
                
            p.write_file()
            p.displayData()    
            
                     
class Patient:
    def __init__(self, data_file_name):
        self.source_file_name = data_file_name
        print("XXX--->",data_file_name)
        with open(data_file_name) as fstream:
            csv_reader = csv.reader(fstream)
            # read patient header
            self.file_header = next(csv_reader)
            self.name = data_file_name.split("-")[-1].split(".")[0].strip()
            self.risk = self.file_header[1]
            #self.age  = self.file_header[2]
            self.age_text = self.file_header[2].partition(' ')[-1]
            self.weight_text = self.file_header[4].partition(' ')[-1]
            self.weight = float(self.weight_text.split()[0])
            # skip blank line
            next(csv_reader)
            # read data header
            self.data_header = next(csv_reader)
            self.datapoints = []
            # read and store rest of file as data
            for row in csv_reader:
                if row[1]:
                    # time data is present (so this is a data row and should be processed)
                    self.datapoints.append(DataPoint(row[0],row[1],row[2],int(row[3]) if row[3] else row[3],row[4]))

    def displayData(self):
        '''print data for this patient'''
        print("Name: {}   Risk: {}   Age: {}   Weight: {}\n\n".format(self.name, self.risk, self.age_text, self.weight_text) \
        + "{0:^3}     {1:^5}     {2:^11}     {3:^5}     {4:^30}\n".format(*self.data_header) \
        + "===     =====     ==========     =====     ==============================\n")
        for dp in self.datapoints:
            print("{0:^3}     {1:^5}     {2:^11}     {3:^5}     {4:^30}".format(dp.day, dp.time, dp.feed, dp.grv, dp.issues))
 

    def write_file(self):
        ''' function to write output file from patient data '''
        with open("RESULT DATA - " + self.name, "w", newline="") as fstream:
            csv_writer = csv.writer(fstream)
            csv_writer.writerow(self.file_header)
            csv_writer.writerow(["","","","",""])
            csv_writer.writerow(self.data_header)
            for dp in self.datapoints:
                csv_writer.writerow(dp.attrList())
            


def main():
    hospital = Hospital()
    hospital.populatePatients()
    hospital.patientFeedingProcess() 
    #Hospital().populatePatients().patientFeedingProcess()

if __name__ == "__main__":
    main()
