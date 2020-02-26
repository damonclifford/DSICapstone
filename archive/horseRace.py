import time as t
import datetime

# Will Daniel, Mo Lu, Winfred Hills
# American Pharaoh won the Triple Crown.  
# He won the Belmont, a 12 furlong track, with a time of 2:26.65,
# the Kentucky Derby, a 10 furlong track, with a time of 2:03.02,
# and the Preakness Stakes, a 9.5 furlong track, with a time of 1.58.46.  
# What was his average speed in mph?

# Output: "[Horses Name] averaged [x] mph across three triple crown races

# Class that stores horse race times and lengths
class Race:    
    
    def __init__(self, time, furlongs=None, miles=None): # constructor
        if type(time) is str: 
            p = datetime.datetime.strptime(time, '%M:%S.%f')
            self.time = datetime.timedelta(0,(p.minute*60 + p.second + p.microsecond/1000000))
        else:
            self.time = time
        if furlongs is None:
            self.furlongs = self.mileToFurlong()
        else:
            self.furlongs = furlongs
        if miles is None:
            self.miles = self.furlongToMile()
        else: 
            self.miles = miles
    
    def furlongToMile(self): # Convert furlongs to miles
        return self.furlongs/8
    
    def mileToFurlong(self): # Convert furlongs to miles
        return self.miles*8
    
    def milesPerHour(self):
        return self.miles / (self.time.total_seconds()/3600)
    
    def __add__(self, other):
        totalTime = self.time + other.time # Fix this to add the numbers
        totalLength = self.furlongs + other.furlongs 
        return Race(totalTime, totalLength)
    
Horse = 'American Paraoh'    
Belmont = Race('02:26.65', 12)
Derby = Race('02:03.02', 10)
Preakness = Race('01:58.46', 9.5)

Total = Belmont + Derby + Preakness

print("{} averaged {} mph across three triple crown races".format(Horse, Total.milesPerHour()))
