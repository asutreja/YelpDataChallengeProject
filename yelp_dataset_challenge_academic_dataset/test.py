import csv
import json
import urllib2
import multiprocessing as mp
from geopy.geocoders import Nominatim
import multiprocessing as mp

check_in_business_id_for_late_night = dict() 
check_in_business_id_for_regular = dict()

user_id_set = set()      # total 366716 unique user ids in this set
cities = set()           # each unique city is stored here

# business_id mapped to # of late night checkins (10 pm to 2 am)
german_business_late_night = dict()  
uk_business_late_night = dict()       
us_business_late_night = dict()       
canada_business_late_night = dict()   

# business_id mapped to # of regular checkins (6 pm to 10 pm)
german_business_regular = dict()  
uk_business_regular = dict()        
us_business_regular = dict()       
canada_business_regular = dict()

# number of businesses stays open very late in each country (closing between 11 pm to 2 am)
german_late_count = 0
uk_late_count = 0
us_late_count = 0
canada_late_count = 0

#writeFile = open('cities', 'w')

# in business csv:
# latitude = 10th column
# longitude = 74th column
# business ID = 16th colomn
# cities = 61st column
# state = 39th column 


# state in UK = EDH, SCB, KHL, ELN, HAM, MLN, FIF, XGL, NTH,
# state in German = BW, RP, NW,   
# state in Canada = ON, QC, 
# state in USA = WA, WI, NC, PA, NV, CA, IL, AZ, MA, MN, SC, OR  

# takes latitude and longitude and returns country name
# def lookup(lat, lon):
#       data = json.load(urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false' % ( str(row[10]), str(row[74]) ) ) )
#       for result in data['results']:
#                       for component in result['address_components']:
#                                       if 'country' in component['types']:
#                                                       return component['long_name']
#       return None

# def findCountry(newMap):
#         global business_id_set
#         global num 

#         coordPair = business_id_set[newMap]
#         geolocator = Nominatim()

#         print num
#         num +=1

#         location = geolocator.reverse(coordPair)
#         if(location.address):
#             business_id_set[newMap] = location.raw['address']['country']
        

# words to look for: Restaurants, Food, Fast Food, Cafes
# hours.Monday.close = 75th column
# hours.Tuesday.close = 77th column
# hours.Wednesday.close = 58th column
# hours.Thursday.close = 47th column
# hours.Friday.close = 41st column
# hours.Saturday.close = 78th column
# hours.Sunday.close = 86th column 

def getBusinessId():
        global canada_business_late_night, us_business_late_night, uk_business_late_night, german_business_late_night
        global german_business_regular, uk_business_regular, us_business_regular, canada_business_regular

        #count = 0

        new_category_set = set()

        with open('yelp_academic_dataset_business.csv', 'rU') as f:
                reader = csv.reader(f)
                next(reader, None) # skipping the header 
                for row in reader: 

                    # code to find the column index in csv file
                    # for each in row:
                    #     if each == 'hours.Sunday.close':
                    #         print each 
                    #         print count
                    #     count+=1 
                    # break

                    temp_business_id = row[16]
                    temp_state = row[39]
                    temp_category = row[9]

                    if temp_category.find('Restaurants') != -1 or temp_category.find('Fast Food') != -1 or temp_category.find('Cafes') != -1 or temp_category.find('Food') != -1:

                        if(temp_state == 'ON' or temp_state == 'QC'):
                            canada_business_late_night[temp_business_id] = 0
                            canada_business_regular[temp_business_id] = 0

                        elif(temp_state == 'BW' or temp_state == 'RP' or temp_state == 'NW'):
                            german_business_late_night[temp_business_id] = 0
                            german_business_regular[temp_business_id] = 0

                        elif(temp_state == 'EDH' or temp_state == 'SCB' or temp_state == 'KHL' or temp_state == 'ELN' or temp_state == 'HAM' or temp_state == 'MLN' or temp_state == 'FIF' or temp_state == 'XGL' or temp_state == 'NTH'):
                            uk_business_late_night[temp_business_id] = 0
                            uk_business_regular[temp_business_id] = 0

                        else:
                            us_business_late_night[temp_business_id] = 0
                            us_business_regular[temp_business_id] = 0


                        #lonLatPair = str(row[10]) + "," + str(row[74])
                        #pairs.append(lonLatPair)
                        #country = findCountry(lonLatPair)
                        #country = lookup( str(row[10]), str(row[74]) )
       

            #if(country == 'United States of America'):
            #   us_business.add(row[16])
            #elif (country == 'United Kingdom'):
                #       uk_business.add(row[16])
                # elif (country == 'Deutschland'):
                #       german_business.add(row[16])
                # elif(country == 'Canada'):
                #       canada_business.add(row[16])
                #cities.add(row[61])

# check-in for 'checkin_info.0-0': 152 column
# check-in for 'checkin_info.0-1': 151 column
# check-in for 'checkin_info.0-2': 154 column
# check-in for 'checkin_info.0-3': 153 column
# check-in for 'checkin_info.0-4': 149 column
# check-in for 'checkin_info.0-5': 148 column
# check-in for 'checkin_info.0-6': 150 column

# check-in for 'checkin_info.1-0': 55 column
# check-in for 'checkin_info.1-1': 32 column
# check-in for 'checkin_info.1-2': 57 column
# check-in for 'checkin_info.1-3': 58 column
# check-in for 'checkin_info.1-4': 59 column
# check-in for 'checkin_info.1-5': 60 column
# check-in for 'checkin_info.1-6': 61 column

# check-in for 'checkin_info.22-0': 36 column
# check-in for 'checkin_info.22-1': 37 column
# check-in for 'checkin_info.22-2': 38 column
# check-in for 'checkin_info.22-3': 39 column
# check-in for 'checkin_info.22-4': 33 column
# check-in for 'checkin_info.22-5': 34 column
# check-in for 'checkin_info.22-6': 35 column

# check-in for 'checkin_info.23-0': 141 column
# check-in for 'checkin_info.23-1': 140 column
# check-in for 'checkin_info.23-2': 143 column
# check-in for 'checkin_info.23-3': 142 column
# check-in for 'checkin_info.23-4': 145 column
# check-in for 'checkin_info.23-5': 144 column
# check-in for 'checkin_info.23-6': 146 column



def getCheckInCountsForLateNight():
    global check_in_business_id

    # business_id is 14th column in checkin.csv
    with open('yelp_academic_dataset_checkin.csv', 'rU') as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            total_checkins = 0
            temp_business_id = row[14]
            
            # counts 12 am to 1 am checkins 
            check0_0 = row[152]
            check0_1 = row[151]
            check0_2 = row[154]
            check0_3 = row[153]
            check0_4 = row[149]
            check0_5 = row[148]
            check0_6 = row[150]

            if(check0_0 != ''):
                total_checkins += int(check0_0)
            if(check0_1 != ''):
                total_checkins += int(check0_1)
            if(check0_2 != ''):
                total_checkins += int(check0_2)
            if(check0_3 != ''):
                total_checkins += int(check0_3)
            if(check0_4 != ''):
                total_checkins += int(check0_4)
            if(check0_5 != ''):
                total_checkins += int(check0_5)
            if(check0_6 != ''):
                total_checkins += int(check0_6)

            # counts 1 am to 2 am checkins 
            check1_0 = row[55]
            check1_1 = row[32]
            check1_2 = row[57]
            check1_3 = row[58]
            check1_4 = row[59]
            check1_5 = row[60]
            check1_6 = row[61]

            if(check1_0 != ''):
                total_checkins += int(check1_0)
            if(check1_1 != ''):
                total_checkins += int(check1_1)
            if(check1_2 != ''):
                total_checkins += int(check1_2)
            if(check1_3 != ''):
                total_checkins += int(check1_3)
            if(check1_4 != ''):
                total_checkins += int(check1_4)
            if(check1_5 != ''):
                total_checkins += int(check1_5)
            if(check1_6 != ''):
                total_checkins += int(check1_6)

            # counts 10 pm to 11 pm checkins
            check22_0 = row[36]
            check22_1 = row[37]
            check22_2 = row[38]
            check22_3 = row[39]
            check22_4 = row[33]
            check22_5 = row[34]
            check22_6 = row[35]

            if(check22_0 != ''):
                total_checkins += int(check22_0)
            if(check22_1 != ''):
                total_checkins += int(check22_1)
            if(check22_2 != ''):
                total_checkins += int(check22_2)
            if(check22_3 != ''):
                total_checkins += int(check22_3)
            if(check22_4 != ''):
                total_checkins += int(check22_4)
            if(check22_5 != ''):
                total_checkins += int(check22_5)
            if(check22_6 != ''):
                total_checkins += int(check22_6)

            # counts 11 pm to 12 am checkins 
            check23_0 = row[141]
            check23_1 = row[140]
            check23_2 = row[143]
            check23_3 = row[142]
            check23_4 = row[145]
            check23_5 = row[144]
            check23_6 = row[146]

            if(check23_0 != ''):
                total_checkins += int(check23_0)
            if(check23_1 != ''):
                total_checkins += int(check23_1)
            if(check23_2 != ''):
                total_checkins += int(check23_2)
            if(check23_3 != ''):
                total_checkins += int(check23_3)
            if(check23_4 != ''):
                total_checkins += int(check23_4)
            if(check23_5 != ''):
                total_checkins += int(check23_5)
            if(check23_6 != ''):
                total_checkins += int(check23_6)

            check_in_business_id_for_late_night[temp_business_id] = total_checkins
            



def getCheckInCountsForRegular():

    count = 0

    with open('yelp_academic_dataset_checkin.csv', 'rU') as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:

            temp_business_id = row[14]
            total_checkins = 0

            # column for 6 pm to 7 pm 
            check18_0 = row[169]
            check18_1 = row[168]
            check18_2 = row[167]
            check18_3 = row[166]
            check18_4 = row[165]
            check18_5 = row[164]
            check18_6 = row[163]

            if(check18_0 != ''):
                total_checkins += int(check18_0)
            if(check18_1 != ''):
                total_checkins += int(check18_1)
            if(check18_2 != ''):
                total_checkins += int(check18_2)
            if(check18_3 != ''):
                total_checkins += int(check18_3)
            if(check18_4 != ''):
                total_checkins += int(check18_4)
            if(check18_5 != ''):
                total_checkins += int(check18_5)
            if(check18_6 != ''):
                total_checkins += int(check18_6)

            # column for 7 pm to 8 pm 
            check19_0 = row[76]
            check19_1 = row[77]
            check19_2 = row[74]
            check19_3 = row[75]
            check19_4 = row[79]
            check19_5 = row[80]
            check19_6 = row[78]

            if(check19_0 != ''):
                total_checkins += int(check19_0)
            if(check19_1 != ''):
                total_checkins += int(check19_1)
            if(check19_2 != ''):
                total_checkins += int(check19_2)
            if(check19_3 != ''):
                total_checkins += int(check19_3)
            if(check19_4 != ''):
                total_checkins += int(check19_4)
            if(check19_5 != ''):
                total_checkins += int(check19_5)
            if(check19_6 != ''):
                total_checkins += int(check19_6)

            # column for 8 pm to 9 pm 
            check20_0 = row[9]
            check20_1 = row[10]
            check20_2 = row[7]
            check20_3 = row[8]
            check20_4 = row[12]
            check20_5 = row[13]
            check20_6 = row[11]

            if(check20_0 != ''):
                total_checkins += int(check20_0)
            if(check20_1 != ''):
                total_checkins += int(check20_1)
            if(check20_2 != ''):
                total_checkins += int(check20_2)
            if(check20_3 != ''):
                total_checkins += int(check20_3)
            if(check20_4 != ''):
                total_checkins += int(check20_4)
            if(check20_5 != ''):
                total_checkins += int(check20_5)
            if(check20_6 != ''):
                total_checkins += int(check20_6)

            # column for 9 pm to 10 pm 
            check21_0 = row[101]
            check21_1 = row[100]
            check21_2 = row[99]
            check21_3 = row[98]
            check21_4 = row[97]
            check21_5 = row[96]
            check21_6 = row[95]

            if(check21_0 != ''):
                total_checkins += int(check21_0)
            if(check21_1 != ''):
                total_checkins += int(check21_1)
            if(check21_2 != ''):
                total_checkins += int(check21_2)
            if(check21_3 != ''):
                total_checkins += int(check21_3)
            if(check21_4 != ''):
                total_checkins += int(check21_4)
            if(check21_5 != ''):
                total_checkins += int(check21_5)
            if(check21_6 != ''):
                total_checkins += int(check21_6)


            check_in_business_id_for_regular[temp_business_id] = total_checkins


def numberOfBusinessesStaysOpenLate():

    global canada_business_late_night, us_business_late_night, uk_business_late_night, german_business_late_night
    global german_late_count, uk_late_count, us_late_count, canada_late_count

    with open('yelp_academic_dataset_business.csv', 'rU') as f:
        reader = csv.reader(f)
        next(reader, None) # skipping the header
        for row in reader:

            temp_business_id = row[16]

            temp_monday_closing =  row[75]
            temp_tuesday_closing = row[77]
            temp_wednesday_closing = row[58]
            temp_thursday_closing = row[47]
            temp_friday_closing = row[41]

            if( (temp_monday_closing == '0:00' or temp_monday_closing == '1:00' or temp_monday_closing == '2:00' or temp_monday_closing == '23:00') and (temp_tuesday_closing == '0:00' or temp_tuesday_closing == '1:00' or temp_tuesday_closing == '2:00' or temp_tuesday_closing == '23:00') and (temp_wednesday_closing == '0:00' or temp_wednesday_closing == '1:00' or temp_wednesday_closing == '2:00' or temp_wednesday_closing == '23:00') and (temp_thursday_closing == '0:00' or temp_thursday_closing == '1:00' or temp_thursday_closing == '2:00' or temp_thursday_closing == '23:00') and (temp_friday_closing == '0:00' or temp_friday_closing == '1:00' or temp_friday_closing == '2:00' or temp_friday_closing == '23:00') ):
                if temp_business_id in us_business_late_night:
                    us_late_count += 1
                elif temp_business_id in uk_business_late_night:
                    uk_late_count += 1
                elif temp_business_id in german_business_late_night:
                    german_late_count += 1
                elif temp_business_id in canada_business_late_night:
                    canada_late_count += 1

def main():

    global canada_business_late_night, german_business_late_night, us_business_late_night, uk_business_late_night
    global check_in_business_id_for_late_night, check_in_business_id_for_regular
    global us_business_regular, uk_business_regular, german_business_regular, canada_business_regular
    global german_late_count, uk_late_count, us_late_count, canada_late_count
    
    us_count = 0
    german_count = 0
    uk_count = 0
    canada_count = 0

    getBusinessId()
    getCheckInCountsForLateNight()
    getCheckInCountsForRegular()


    # assigning total late night check-ins based on business id's
    for i in check_in_business_id_for_late_night.keys():

        if(us_business_late_night.has_key(i)):
            us_business_late_night[i] = check_in_business_id_for_late_night[i]
        elif(uk_business_late_night.has_key(i)):
            uk_business_late_night[i] = check_in_business_id_for_late_night[i]
        elif(canada_business_late_night.has_key(i)):
            canada_business_late_night[i] = check_in_business_id_for_late_night[i]
        elif(german_business_late_night.has_key(i)):
            german_business_late_night[i] = check_in_business_id_for_late_night[i]

    # adding total late night check-ins    
    for i in us_business_late_night.keys():
        us_count += us_business_late_night[i]

    for i in german_business_late_night.keys():
        german_count += german_business_late_night[i]

    for i in canada_business_late_night.keys():
        canada_count += canada_business_late_night[i]

    for i in uk_business_late_night.keys():
        uk_count += uk_business_late_night[i]




    # pool = mp.Pool(processes=5)
    # pool.map( findCountry, business_id_set )
   
    #business_id_set[ business_id_set.keys()[0] ] = "Hello"
    #print business_id_set

    print
    print "****************************"
    print "Number of Restaurants in dataset by countries: "
    print "****************************"
    print "UK -> %d" % len(uk_business_late_night)
    print "US -> %d" % len(us_business_late_night)
    print "Canada -> %d" % len(canada_business_late_night)
    print "Germany -> %d" % len(german_business_late_night)
    print
    print

    print "****************************"
    print "Number of Late Night check-ins (10 pm to 2 am) by countries:"
    print "****************************"
    print "UK -> %d" % uk_count
    print "US -> %d" % us_count
    print "Canada -> %d" % canada_count
    print "German -> %d" % german_count
    print
    print

    us_count = 0
    german_count = 0
    uk_count = 0
    canada_count = 0


    # assigning total regular check-ins based on business id's
    for i in check_in_business_id_for_regular.keys():

        if(us_business_regular.has_key(i)):
            us_business_regular[i] = check_in_business_id_for_regular[i]
        elif(uk_business_regular.has_key(i)):
            uk_business_regular[i] = check_in_business_id_for_regular[i]
        elif(canada_business_regular.has_key(i)):
            canada_business_regular[i] = check_in_business_id_for_regular[i]
        elif(german_business_regular.has_key(i)):
            german_business_regular[i] = check_in_business_id_for_regular[i]

    # adding total late night check-ins    
    for i in us_business_regular.keys():
        us_count += us_business_regular[i]

    for i in german_business_regular.keys():
        german_count += german_business_regular[i]

    for i in canada_business_regular.keys():
        canada_count += canada_business_regular[i]

    for i in uk_business_regular.keys():
        uk_count += uk_business_regular[i]


    print "****************************"
    print "Number of Normal time check-ins (6 pm to 10 pm) by countries: "
    print "****************************"
    print "UK -> %d" % uk_count
    print "US -> %d" % us_count
    print "Canada -> %d" % canada_count
    print "German -> %d" % german_count
    print
    print

    numberOfBusinessesStaysOpenLate()

    print "****************************"
    print "Number of Restaurants stays open late (closes between 11 pm and 2 am) by countries: "
    print "****************************"
    print "UK -> %d" % uk_late_count
    print "US -> %d" % us_late_count
    print "Canada -> %d" % canada_late_count
    print "German -> %d" % german_late_count
    print 
    print
    print "****************************"


main()



# with open('yelp_academic_dataset_user.csv', 'rU') as f:
#       reader = csv.reader(f)
#       for row in reader:
#               user_id_set.add(row[16])

 



#for x in cities:
#       writeFile.write(str(x) + "\n")

#writeFile.close()

#print business_id_set
# print "number of businesses in Canada: %d" % len(canada_business)
# print "****************************"
# print "number of businesses in UK: %d" % len(uk_business)
# print "****************************"
# print "number of businesses in Germany: %d" % len(german_business)
# print "****************************"
# print "number of businesses in US: %d" % len(us_business)
# print "****************************"







#print user_id_set