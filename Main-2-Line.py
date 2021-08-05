#################################################
### This program downloads the NORAD 2-Line
### elements for the International Space Station
### and extracts key data from them. It then 
### calculates classical orbital elements
### from that data.
###
### Change 1 (This comment only)
#################################################
import requests
import numpy as np
import math


# The following section accesses the text file with the 2-Line elements
# from the web and copies its  contetnts into
# a local text file used for later analysis

url_target = "http://www.celestrak.com/NORAD/elements/stations.txt"
output_file = "/Users/williamshavce/Library/Mobile Documents/com~apple~CloudDocs/Programming/Python Files/file.txt"
#print (url_target)
print (output_file)

ISS_ID = "25544U"
ISS_ID_LINE2 = "25544 "
Mu = 3.986005e5 #Gravitational Parameter in Km^3/sec^2
REarth = 6378.137 #Mean Earth Radius in Km
TwoLine = ""

#set variable r to webpage content of url_target
#opens output_file for writing as variable f
#wries the content of webpage at r to file f
r = requests.get(url_target)
with open(output_file, 'wb') as f:
	f.write(r.content)
file1 = open(output_file, "r")

#Create string called "TwoLine" from the contents of the text file
TwoLine = open(output_file, 'r').read()

# Create a single string to hold the information
# for the 2-Line elements
print (TwoLine)
#print ("\nNumber of Characters: ", len(TwoLine))

#Find the starting location of the ISS data for Line 1 in the string TwoLine
location = int(TwoLine.find(ISS_ID))
#print (ISS_ID, " found at index: ", location)

#Extract Epoch Year, Line 1, 19-20
Epoch_Yr = int(TwoLine[location + 16:location + 17])
print ("\nEpoch Year: ",Epoch_Yr)

#Determine if current Epoch Year is a Leap Year
if Epoch_Yr % 4 == 0:
    LeapYr = True
else:
    LeapYr = False
#if LeapYr:
#    print("This is a Leap Year")
#else:
#    print("This is not a Leap Year")
    
#Extract Epoch Day, Line 1, 21-32
Epoch_Day = float(TwoLine[location + 18:location + 29])
print ("Epoch Day: ",Epoch_Day)


Epoch_Day_Int = math.trunc(Epoch_Day)
print ("Day of Year: ", Epoch_Day_Int)

Epoch_Day_Fraction = Epoch_Day - Epoch_Day_Int
#print ("Fraction of Day: ", format(Epoch_Day_Fraction, ".8f"))
Hour_of_Day = Epoch_Day_Fraction * 24
Minutes = (Hour_of_Day - math.trunc(Hour_of_Day)) * 60
print ("Time: ", math.trunc(Hour_of_Day))
print ("Minutes: ", math.trunc(Minutes))
Seconds = (Minutes - math.trunc(Minutes)) * 60
print ("Seconds: ", format(Seconds, ".1f"))

#Extract First Derivative of Mean Motion (Ballistic Coefficient), Line 1, 34-43
Ballistic_Coef = float(TwoLine[location + 31:location + 40])
print ("Ballistic Coefficient: ", Ballistic_Coef)

#Extract Second Derivative of Mean Motion, Line 1, 45-52
Sec_Der_Mean_Motion = TwoLine[location + 42:location + 49]
print ("Second Derivative of Mean Motion: ", Sec_Der_Mean_Motion)

#Extract Radiation Pressure Coefficient, B-Star, Line 1, 54-61
BStar = TwoLine[location + 51:location + 58]
print ("B-Star: ", BStar)

#Extract Element Set Number, Line 1, 65-68
El_Set = int(TwoLine[location + 62:location + 65])
print ("Element Set Number: ", El_Set)

#Find the starting location of the ISS data for Line 2 in the string TwoLine
location = int(TwoLine.find(ISS_ID_LINE2))
#print (ISS_ID_LINE2, " found at index: ", location)

#Extract Orbital Inclination at Epoch, Line 2, 9-16
Inclination = float(TwoLine[location+6:location+13])
print ("Inclination: ", Inclination)

#Extract Right Ascension of Ascending Node, Line 2, 18-25
RA_Asc_Node = float(TwoLine[location+15:location+22])
print ("Right Ascension of Ascending Node: ", RA_Asc_Node)

#Extract Orbital Eccentricity, Line 2, 27-33
Eccentricity = float("." + (TwoLine[location+24:location+30]))
print ("Orbital Eccentricity: ", Eccentricity)

#Extract Argument of Perigee at Epoch, Line 2, 35-42
Arg_of_Perigee = float(TwoLine[location+32:location+39])
print ("Argument of Perigee: ", Arg_of_Perigee)

#Extract Mean Anomaly at Epoch, Line 2, 44-51
Mean_Anomaly = float(TwoLine[location+41:location+48])
print ("Mean Anomaly: ", Mean_Anomaly)

#Extract Mean Motion (Revs per Day), Line 2, 53-63
Mean_Motion = float(TwoLine[location+50:location+60])
print ("Mean Motion: ", format(Mean_Motion, ".2f"), " Revolutions per Day")

#Extract Revolution Number at Epoch, Line 2, 64-68
Rev_Number = int(TwoLine[location+61:location+66])
print ("Revolution Number at Epoch: ", Rev_Number, " Revolutions")

file1.close

# This section uses the extracted information to 
# calculate the classic orbital elements
# for the ISS
# Classic Orbital Elements:
# a: Semi-Major Axis (Calculated)
# e: Eccentricity (Listed in 2-Line)
# i: Inclination (Listed in 2-Line)
# Omega: RA of Ascending Node (Listed in 2-Line)
# w: Argument of Perigee (Listed in 2-Line)
# nu: True Anomaly (calculated)

n = Mean_Motion * 2 * np.pi
n = n / 86400
print ("Mean Motion of Orbit:", format(n, ".5f"), "Radians per Second")

#Calculate Semi-Major Axis
a = (Mu / (n**2)) ** (1/3)
print ("Semi-Major Axis:", format(a, ".3f"), "Km")

#Calculate 1/2 Focus Distance
c = a * Eccentricity
print ("One-Half Focus Distance:",format(c, ".0f"), "Km")

#Calculate Semi-Minor Axis
b = a * ((1 - Eccentricity**2)**.5)
print ("Semi-Minor Axis:", format(b, ".3f"), "Km")

#Calculate Altitude
altitude = a - REarth
print ("Average Altitude:", format(altitude, ".0f"), "Km")
print ("Average Altitude:", format(altitude * 0.621371, ".0f"), "Miles")

#Calculate Orbital Period in minutes
Period = (2 * np.pi / n) / 60
print ("Orbital Period:", format(Period, ".1f"), "Minutes,", format(Period/60, ".3f"), "Hours")

#Calculate semi-latus rectum in Km
P = a * (1 - Eccentricity**2)
print ("Semi-Latus Rectum:", format(P, ".1f"), "Km")

#Calculate Velocity at apogee
Va = ((Mu / a) * ((1 - Eccentricity) / (1 + Eccentricity))) ** .5
print ("Velocity at apogee:", format(Va, ".3f"), "Km/sec")

#Calculate Velocity at perigee
Vp = ((Mu / a) * ((1 + Eccentricity) / (1 - Eccentricity))) ** .5
print ("Velocity at perigee:", format(Vp, ".3f"), "Km/sec")

#Calculate Mean Anomaly in radians
Mean_Anomaly_Radians = Mean_Anomaly * (math.pi / 180)
print ("Mean Anomaly:", format(Mean_Anomaly_Radians, ".3f"), "Radians")

#Calculate Eccentric Anomaly
E1 = Mean_Anomaly_Radians + Eccentricity * math.sin(Mean_Anomaly_Radians)
E2 = Mean_Anomaly_Radians + Eccentricity * math.sin(E1)
E3 = Mean_Anomaly_Radians + Eccentricity * math.sin(E2)
E4 = Mean_Anomaly_Radians + Eccentricity * math.sin(E3)
E5 = Mean_Anomaly_Radians + Eccentricity * math.sin(E4)
E6 = Mean_Anomaly_Radians + Eccentricity * math.sin(E5)
E7 = Mean_Anomaly_Radians + Eccentricity * math.sin(E6)
E8 = Mean_Anomaly_Radians + Eccentricity * math.sin(E7)
E9 = Mean_Anomaly_Radians + Eccentricity * math.sin(E8)
E10 = Mean_Anomaly_Radians + Eccentricity * math.sin(E9)
Eccentric_Anomaly = E10
print("Eccentric Anomaly:", format(Eccentric_Anomaly, ".3f"), "Radians")

#Calculate True Anomaly
True_Anomaly = math.acos((math.cos(Eccentric_Anomaly)-Eccentricity) / (1 - (Eccentricity * math.cos(Eccentric_Anomaly))))
print("True Anomaly:", format(True_Anomaly,".3f"), "Radians")
True_Anomaly_Deg = True_Anomaly * (180/math.pi)
print("True Anomaly", format(True_Anomaly_Deg,".2f"),"Degrees")

#Calculate radius to satellite at epoch
Radius = P / (1 + Eccentricity * math.cos(True_Anomaly_Deg))
print("Current Radius:", format(Radius,".3f"),"Km")
print("Current Altitude:", format((Radius-REarth),".0f"), "Km")
print("Current Altitude:",format(((Radius-REarth)* 0.621371),".0f"), "Miles")

#Calculate velocity of satellite at epoch
Velocity = (Mu * (2/Radius - 1/a))**.5
print("Current Verlocity:", format(Velocity,".3f"),"Km/sec")
print("Current Verlocity:", format(Velocity * .691371 * 3600,".0f"),"MpH")

#Calculate Flight Path Angle
Phi = math.atan((Eccentricity+math.sin(True_Anomaly_Deg))/(1+Eccentricity*math.cos(True_Anomaly_Deg)))
print("Flight Path Angle:", format(Phi,".3f"), "Degrees")

#Calculate Specific Mechanical Energy of Orbit
E = - (Mu / (2 * a))
print ("Specific Mechanical Energy:", format(E,".2f"),"Km^2/sec^2")
