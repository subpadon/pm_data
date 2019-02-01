#!/usr/bin/env python
# coding: utf-8

# This code extracts data from the air4thai
#
# http://air4thai.pcd.go.th/webV2/history/api/data.php?stationID=03t&param=PM25&type=hr&sdate=2019-01-17&edate=2019-01-17

import requests
from datetime import date, datetime, timedelta
import pandas as pd

station_list = [
    '02t', '03t', '05t', '08t', '10t',
    '11t', '12t', '13t', '14t', '16t', '17t', '18t', '19t',
    '20t', '21t', '22t', '24t', '25t', '26t', '27t', '28t', '29t',
    '30t', '31t', '32t', '33t', '34t', '35t', '36t', '37t', '38t', '39t',
    '40t', '41t', '42t', '43t', '44t', '46t', '47t',
    '50t', '52t', '53t', '54t', '57t', '58t', '59t',
    '60t', '61t', '62t', '63t', '67t', '68t', '69t',
    '70t', '71t', '72t', '73t', '74t', '75t', '76t', '77t', '79t',
    '80t'
]

measured_list = ['PM25', 'PM10', 'O3', 'CO', 'NO2', 'SO2']
#measured_list = ['SO2']

for del_day in range(1,31):
    ytd = str(date.today()-timedelta(del_day))    # get yesterday's date
    print(ytd)
    meas_dat = []
    meas_dat = pd.DataFrame()

    for meas in measured_list :             # loop over each measurement

        pm = []
        tm = []
        dt = []
        stn= []

        for stn_i in station_list :             # loop over each station


            url = 'http://air4thai.pcd.go.th/webV2/history/api/data.php?stationID=' + stn_i + '&param=' + meas + '&type=hr&sdate=' + ytd + '&edate=' + ytd

            data = requests.request("GET", url).json()

            if data['stations'] == []:
                val_data = data

                for each in list(range(0,24)):

                    DT_obj = datetime.strptime(ytd, '%Y-%m-%d')
                    #print(each)
                    DT_obj = DT_obj.replace(hour=each)
                    #print(DT_obj)
                    DT_str = DT_obj.strftime('%Y-%m-%d %H:%M:%S')

                    time_dat = DT_str

                    date_str = time_dat[0:10]
                    time_str = time_dat[11:]

                    pm.append(None)
                    tm.append(time_str)
                    dt.append(date_str)
                    stn.append(stn_i)

            else :
                val_data = data['stations'][0]['data']


                for each in val_data :          # loop over each time stamp
                    time_dat = each['DATETIMEDATA']
                    date_str = time_dat[0:10]
                    time_str = time_dat[11:]

                    tm.append(time_str)
                    dt.append(date_str)

                    val_dat  = each[meas]
                    if val_dat == '-' :
                        val_dat = None
                    pm.append(val_dat)
                    stn.append(stn_i)
        meas_dat['station'] = stn
        meas_dat['date'] = dt
        meas_dat['time'] = tm
        meas_dat[meas] = pm

    meas_dat.to_csv('~/Documents/pm25/pm_data_30days/pm_data_'+ytd+'.csv', encoding='utf-8')
