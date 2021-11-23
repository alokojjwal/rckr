import time
start_time = time.time()
import pandas as pd
# import json
import requests
from math import sin, cos, sqrt, radians, asin

R = 6371.0

# function for sorting in ascending order
def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li

# conversion of downloaded json file to csv file
# # dat_f = open('countriesV2.json','r', encoding='utf-8')
# # dat = json.loads(dat_f.read())

# # df = pd.json_normalize(dat)

# conversion of json file realtime into csv
url_d='https://cdn.jsdelivr.net/gh/apilayer/restcountries@3dc0fb110cd97bce9ddf27b3e8e1f7fbe115dc3c/src/main/resources/countriesV2.json'

res=requests.get(url_d).json()

df=pd.DataFrame(res)

df.to_csv('countriesV2.csv', encoding='utf-8', index=False)


# replacing the vacant latitudes and longitudes
for i in range(0,len(df['latlng'])):
    if(df['latlng'][i]==[]):
        df['latlng'][i]=[0.000,0.000]

# limiting the population above a limit
Lt_List=[]
for i in range(0,len(df['population'])):
    if(df['population'][i]>=550):
        Lt_List.append([df['latlng'][i],df['population'][i],df['name'][i]])

# sorting the rows in order of increasing population above the limit
Sort(Lt_List)

# making a list of 20 latitudes and longitudes poping out from the list
Lat_List=[]
for i in range(0,20):
    Lat_List.append(Lt_List[i][0])
    
# calculation of the distances between any two points and summation of theirs

distance=0

for i in range(0,19):
    for j in range(i+1,20):
        lat1 = radians(Lat_List[i][0])
        lon1 = radians(Lat_List[i][1])
        lat2 = radians(Lat_List[j][0])
        lon2 = radians(Lat_List[j][1])
    
        dlon = lon2 - lon1
        dlat = lat2 - lat1
    
# harvesian formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        
        dist = R * c
        
        distance = distance + round(dist,2)
end_time=time.time()
time_taken=end_time-start_time