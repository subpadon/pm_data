# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:04:01 2019

@author: pond
"""


import requests#,folium
import pandas as pd
#import numpy as np

usr  = 'u62peeradon.sam'
ukey = 'bee7b411594460fd1ff84d89ec450ee7'

r = requests.get('https://data.tmd.go.th/api/Weather3Hours/V2/?uid=' + usr + '&ukey=' + ukey + '&format=json')


#print(r.text)
doc = eval(r.text)

header_doc = doc['Header']
station_dat = doc['Stations']['Station']

# Loop over nested field, in this case, Observation
ObsKeys = station_dat[0]['Observation']
ObsVal  = []
for row in station_dat:
  ObsKeys = row['Observation']
  obs_each_row = [row['WmoStationNumber']]
  for key, val in ObsKeys.items():
    obs_each_row.append(val)
  ObsVal.append(obs_each_row)

dfObs = pd.DataFrame(ObsVal, columns = ['WmoStationNumber'] + list(ObsKeys.keys()))

print(dfObs)

df1 = pd.DataFrame.from_dict(station_dat)

df1 = df1.drop('Observation', 1)
df1 = df1[['WmoStationNumber', 'StationNameEnglish', 'StationNameThai', 'Province', 'Latitude', 'Longitude']]

dfOut = df1.merge(dfObs)

# seperate date and time field
df_DT = dfOut['DateTime'].str.split(' ', n=1, expand=True)
df_DT[0] = df_DT[0].str.replace('\\\/', '-')
dfOut.insert(7, 'Date', df_DT[0])
dfOut.insert(8, 'Time', df_DT[1])
dfOut = dfOut.drop('DateTime', 1)


#dfOut.set_index(dfOut['WmoStationNumber'], inplace = True)
print(dfOut)

date_str = dfOut.iloc[-1]['Date']
time_str = dfOut.iloc[-1]['Time'].replace(':', '-')

outname = 'data/' + date_str + '_' + time_str + '.csv'
dfOut.to_csv(outname, index=False)